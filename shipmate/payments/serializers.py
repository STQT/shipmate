from django.db.models import Sum
from rest_framework import serializers

from shipmate.contrib.serializers import Base64ImageField
from shipmate.payments.models import OrderPayment, OrderPaymentAttachment


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
    image = Base64ImageField(use_url=True)

    class Meta:
        model = OrderPaymentAttachment
        fields = ['order_payment', 'amount', 'image']

    def create(self, validated_data):
        order_payment: OrderPayment = validated_data['order_payment']
        order_payment_attachments_all_amount = OrderPaymentAttachment.objects.filter(order_payment=order_payment)
        total_amount = order_payment_attachments_all_amount.aggregate(Sum('amount'))['amount__sum'] or 0
        order_payment.amount_charged = total_amount + validated_data['amount']
        if order_payment.amount <= order_payment.amount_charged:
            order_payment.status = OrderPayment.StatusChoices.PAID
        order_payment.save()
        return OrderPaymentAttachment.objects.create(**validated_data)
