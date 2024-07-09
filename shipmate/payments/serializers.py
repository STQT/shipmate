from rest_framework import serializers

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
    class Meta:
        model = OrderPaymentAttachment
        fields = ['order_payment', 'amount', 'image']


class CreateOrderPaymentAttachmentListSerializer(serializers.Serializer):
    attachments = OrderPaymentAttachmentSerializer(many=True)

    def create(self, validated_data):
        attachments_data = validated_data.pop('attachments')
        attachments = [OrderPaymentAttachment(**item) for item in attachments_data]
        return OrderPaymentAttachment.objects.bulk_create(attachments)
