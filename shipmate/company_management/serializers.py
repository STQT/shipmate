from rest_framework import serializers
from .models import (
    CompanyInfo, CompanyInfoLog, MerchantLog,
    VoIPLog, VoIP, Template, Merchant, TemplateLog,
    PaymentAppLog, PaymentApp, LeadParsingGroup,
    LeadParsingItem, LeadParsingValue
)


class CompanyInfoLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInfoLog
        fields = ("title", "message")


class MerchantLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantLog
        fields = ("title", "message")


class VoIPLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoIPLog
        fields = ("title", "message")


class TemplateLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateLog
        fields = ("title", "message")


class PaymentAppLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentAppLog
        fields = ("title", "message")


class CompanyInfoSerializer(serializers.ModelSerializer):
    logs = CompanyInfoLogSerializer(many=True, read_only=True)

    class Meta:
        model = CompanyInfo
        fields = "__all__"


class MerchantSerializer(serializers.ModelSerializer):
    logs = MerchantLogSerializer(many=True, read_only=True)

    class Meta:
        model = Merchant
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data = self.blur_sensitive_fields(data)
        return data

    def blur_sensitive_fields(self, data):
        sensitive_fields = [
            'authorize_login',
            'authorize_password',
            'authorize_pin_code',
            'firstdata_gateway_id',
            'firstdata_password',
            'firstdata_key_id',
            'firstdata_hmac_key',
            'paypal_secret_key',
        ]

        for field in sensitive_fields:
            if field in data and data[field]:
                data[field] = self.blur_value(data[field])

        return data

    def blur_value(self, value):
        if isinstance(value, str):
            blurred_part = "*" * (len(value) - 4) + value[-4:]
            return blurred_part
        return value


class VoIPSerializer(serializers.ModelSerializer):
    logs = VoIPLogSerializer(many=True, read_only=True)

    class Meta:
        model = VoIP
        fields = "__all__"


class TemplateSerializer(serializers.ModelSerializer):
    updated_from_email = serializers.StringRelatedField(source='updated_from.email', read_only=True)
    logs = TemplateLogSerializer(many=True, read_only=True)

    class Meta:
        model = Template
        fields = "__all__"


class PaymentAppSerializer(serializers.ModelSerializer):
    updated_from_email = serializers.StringRelatedField(source='updated_from.email', read_only=True)
    logs = PaymentAppLogSerializer(many=True, read_only=True)

    class Meta:
        model = PaymentApp
        fields = "__all__"


class LeadParsingValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadParsingValue
        fields = ['id', 'value']


class LeadParsingItemSerializer(serializers.ModelSerializer):
    values = LeadParsingValueSerializer(many=True)

    class Meta:
        model = LeadParsingItem
        fields = ['id', 'name', 'values']


class LeadParsingSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadParsingItem
        fields = ['id', 'name', ]


class LeadParsingGroupSerializer(serializers.ModelSerializer):
    items = LeadParsingItemSerializer(many=True, source='values')

    class Meta:
        model = LeadParsingGroup
        fields = ['id', 'name', 'items']


class CreateLeadParsingValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadParsingValue
        fields = "__all__"
