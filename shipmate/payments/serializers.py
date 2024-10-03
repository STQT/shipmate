from django.db import transaction
from django.db.models import Sum
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from shipmate.contrib.authorize import charge_payment, refund_payment
from shipmate.contrib.models import Attachments
from shipmate.contrib.serializers import Base64ImageField
from shipmate.orders.models import OrderAttachment
from shipmate.orders.serializers import CompanyDetailInfoSerializer, RetrieveOrderSerializer
from shipmate.payments.models import OrderPayment, OrderPaymentAttachment, OrderPaymentCreditCard, TypeChoices


class DetailContractSerializer(serializers.Serializer):
    # order = RetrieveOrderSerializer(read_only=True)
    # contract = OrderPaymentSerializer(read_only=True)
    # company = CompanyDetailInfoSerializer(read_only=True)
    # pdf = BaseContractSerializer(read_only=True)
    ...


class SigningContractSerializer(serializers.ModelSerializer):
    agreement = serializers.FileField(write_only=True)
    terms = serializers.FileField(write_only=True)

    class Meta:
        model = OrderPayment
        exclude = ("created_at", "order", "contract_type")
        read_only_fields = ["sign_ip_address", "signed_time", "signed"]


class CreateOrderPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPayment
        exclude = ("status", "amount_charged")


class OrderPaymentSerializer(serializers.ModelSerializer):
    executed_on = serializers.SerializerMethodField()

    class Meta:
        model = OrderPayment
        fields = "__all__"

    @classmethod
    def get_executed_on(cls, obj) -> str:
        if obj.created_at:
            return obj.created_at.strftime("%m/%d/%Y")
        return "NaN"


class OrderPaymentAttachmentSerializer(serializers.ModelSerializer):
    image = Base64ImageField(use_url=True, required=False, allow_null=True)
    credit_card = serializers.IntegerField(allow_null=True, write_only=True, required=False)

    class Meta:
        model = OrderPaymentAttachment
        fields = ['id', 'order_payment', 'amount', 'image', 'payment_type',
                  'created_at', 'is_success', 'credit_card', 'transaction_id']
        extra_kwargs = {
            'is_success': {'read_only': True},
            'payment_type': {'read_only': True},
        }

    @transaction.atomic
    def create(self, validated_data):
        order_payment: OrderPayment = validated_data['order_payment']
        amount = validated_data['amount']
        validated_data['payment_type'] = order_payment.payment_type
        credit_card = validated_data.pop("credit_card")
        if credit_card:
            try:
                credit_card: OrderPaymentCreditCard = OrderPaymentCreditCard.objects.get(pk=credit_card)
            except OrderPaymentCreditCard.DoesNotExist:
                raise ValidationError({"credit_card": "Does not found this Credit Card object in DB"})
            result = charge_payment(amount, credit_card.card_number, credit_card.expiration_date, credit_card.cvv)
            if result['success'] is False:
                validated_data['is_success'] = False
                OrderPaymentAttachment.objects.create(**validated_data)
                raise ValidationError({"credit_card": f"Problem via Authorize.net: {result['message']}"})
            validated_data['transaction_id'] = result['transaction_id']
            validated_data['credit_card'] = credit_card.pk
        order = order_payment.order
        order.payment_carrier_pay = order.payment_carrier_pay + amount
        order.save()
        order_payment_attachments_all_amount = OrderPaymentAttachment.objects.filter(order_payment=order_payment)
        total_amount = order_payment_attachments_all_amount.aggregate(Sum('amount'))['amount__sum'] or 0
        order_payment.amount_charged = total_amount + amount
        OrderAttachment.objects.create(
            order=order,
            second_title=OrderPayment.DirectionChoices(order_payment.direction).label,
            type=Attachments.TypesChoices.ACTIVITY,
            title=f"${order_payment.amount_charged} is made by {'Credit Card' if credit_card else TypeChoices(order_payment.payment_type).label}",
            link=0,
            user=order.user
        )
        if order_payment.amount <= order_payment.amount_charged:
            order_payment.status = OrderPayment.StatusChoices.PAID
        order_payment.save()
        return OrderPaymentAttachment.objects.create(**validated_data)


class RefundPaymentSerializer(serializers.ModelSerializer):
    transaction_id = serializers.IntegerField()
    amount = serializers.FloatField()

    class Meta:
        model = OrderPayment
        fields = ["amount", "direction", "transaction_id", "order"]

    def create(self, validated_data):
        transaction_id = validated_data.pop('transaction_id')
        amount = validated_data['amount']
        try:
            transaction = OrderPaymentAttachment.objects.get(transaction_id=transaction_id)
        except:
            raise ValidationError({"transaction_id": "Not found transaction"})
        validated_data['name'] = OrderPayment.NameChoices.auto_transportation
        validated_data['quantity'] = 1
        validated_data['amount_charged'] = -amount
        validated_data['discount'] = 0
        validated_data['payment_type'] = TypeChoices.credit_card
        validated_data['surcharge_fee_rate'] = 5
        validated_data['charge_type'] = OrderPayment.ChargeTypeChoices.refund
        validated_data['status'] = OrderPayment.StatusChoices.PAID
        order_payment = OrderPayment.objects.create(**validated_data)
        if transaction.credit_card:
            refund_payment(amount, transaction_id, transaction.credit_card.card_number,
                           transaction.credit_card.expiration_date)
            return order_payment
        raise ValidationError({"transaction_id": "Not found card number from this transaction"})


def blur_card_number(card_number):
    if len(card_number) >= 4:
        blurred_part = "*" * (len(card_number) - 4) + card_number[-4:]
    else:
        blurred_part = "*" * len(card_number)
    return blurred_part


class ListOrderPaymentCreditCardSerializer(serializers.ModelSerializer):
    card_number = serializers.SerializerMethodField()
    cvv = serializers.SerializerMethodField()

    class Meta:
        model = OrderPaymentCreditCard
        fields = "__all__"

    def get_card_number(self, obj):
        card_number = obj.card_number
        blurred_card_number = blur_card_number(card_number)
        return blurred_card_number

    def get_cvv(self, obj):
        cvv = obj.cvv
        blurred_card_number = blur_card_number(cvv)
        return blurred_card_number



class CreateOrderPaymentCreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPaymentCreditCard
        fields = "__all__"


class CreateOrderPaymentClientCreditCardSerializer(serializers.ModelSerializer):
    sign_file = Base64ImageField(use_url=True, required=False, allow_null=True)
    cc_front_img_file = serializers.ImageField(write_only=True, required=False, allow_null=True, allow_empty_file=True)
    cc_back_img_file = serializers.ImageField(write_only=True, required=False, allow_null=True, allow_empty_file=True)

    class Meta:
        model = OrderPaymentCreditCard
        fields = "__all__"

class OrderPaymentViewSerializer(serializers.Serializer):
    amount = serializers.FloatField()
    surcharge_fee_rate = serializers.IntegerField()
    discount = serializers.FloatField()


class DetailCustomerPaymentSerializer(serializers.Serializer):
    order = RetrieveOrderSerializer(read_only=True)
    company = CompanyDetailInfoSerializer(read_only=True)
    cc = serializers.BooleanField(read_only=True)
    payment = OrderPaymentViewSerializer(many=False, allow_null=True)
