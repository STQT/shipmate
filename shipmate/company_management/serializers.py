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
        fields = ['name', 'values']


class LeadParsingGroupSerializer(serializers.ModelSerializer):
    items = LeadParsingItemSerializer(many=True, source='values')

    class Meta:
        model = LeadParsingGroup
        fields = ['name', 'items']
