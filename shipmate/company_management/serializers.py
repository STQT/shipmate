from rest_framework import serializers
from .models import CompanyInfo, CompanyInfoLog


class CompanyInfoLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInfoLog
        fields = ("title", "message")


class CompanyInfoSerializer(serializers.ModelSerializer):
    logs = CompanyInfoLogSerializer(many=True, read_only=True)

    class Meta:
        model = CompanyInfo
        fields = "__all__"
