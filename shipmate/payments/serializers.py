from django.db.models import Sum
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from shipmate.contrib.authorize import charge_payment
from shipmate.contrib.serializers import Base64ImageField
from shipmate.payments.models import OrderPayment, OrderPaymentAttachment, OrderPaymentCreditCard


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
    image = Base64ImageField(use_url=True, required=False)
    credit_card = serializers.IntegerField(allow_null=True, write_only=True, required=False)

    class Meta:
        model = OrderPaymentAttachment
        fields = ['order_payment', 'amount', 'image', 'payment_type', 'created_at', 'is_success', 'credit_card']
        extra_kwargs = {
            'is_success': {'read_only': True},
            'payment_type': {'read_only': True},
        }
    def create(self, validated_data):
        order_payment: OrderPayment = validated_data['order_payment']
        amount = validated_data['amount']
        validated_data['payment_type'] = order_payment.payment_type
        credit_card = validated_data.pop("credit_card")
        if credit_card:
            credit_card: OrderPaymentCreditCard = OrderPaymentCreditCard.objects.get(pk=credit_card)
            result = charge_payment(amount, credit_card.card_number, credit_card.expiration_date, credit_card.cvv)
            if result['success'] is False:
                validated_data['is_success'] = False
                OrderPaymentAttachment.objects.create(**validated_data)
                raise ValidationError({"credit_card": f"Problem via Authorize.net: {result['message']}"})
        order_payment_attachments_all_amount = OrderPaymentAttachment.objects.filter(order_payment=order_payment)
        total_amount = order_payment_attachments_all_amount.aggregate(Sum('amount'))['amount__sum'] or 0
        order_payment.amount_charged = total_amount + amount
        if order_payment.amount <= order_payment.amount_charged:
            order_payment.status = OrderPayment.StatusChoices.PAID
        order_payment.save()
        return OrderPaymentAttachment.objects.create(**validated_data)


def blur_card_number(card_number):
    if len(card_number) >= 4:
        blurred_part = "*" * (len(card_number) - 4) + card_number[-4:]
    else:
        blurred_part = "*" * len(card_number)
    return blurred_part


class ListOrderPaymentCreditCardSerializer(serializers.ModelSerializer):
    card_number = serializers.SerializerMethodField()

    class Meta:
        model = OrderPaymentCreditCard
        fields = "__all__"

    def get_card_number(self, obj):
        card_number = obj.card_number
        blurred_card_number = blur_card_number(card_number)
        return blurred_card_number


class CreateOrderPaymentCreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPaymentCreditCard
        fields = "__all__"
