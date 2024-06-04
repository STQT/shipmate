from rest_framework import serializers
from .models import CompanyInfo, CompanyInfoLog, MerchantLog, VoIPLog, VoIP


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


class CompanyInfoSerializer(serializers.ModelSerializer):
    logs = CompanyInfoLogSerializer(many=True, read_only=True)

    class Meta:
        model = CompanyInfo
        fields = "__all__"


class MerchantSerializer(serializers.ModelSerializer):
    logs = MerchantLogSerializer(many=True, read_only=True)

    class Meta:
        model = MerchantLog
        fields = "__all__"


class VoIPSerializer(serializers.ModelSerializer):
    logs = VoIPLogSerializer(many=True, read_only=True)

    class Meta:
        model = VoIP
        fields = "__all__"
