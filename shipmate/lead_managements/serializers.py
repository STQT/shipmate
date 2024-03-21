from rest_framework import serializers

from shipmate.lead_managements.models import Provider, ProviderLog


class ProviderLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderLog
        fields = ("title", "message")


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = "__all__"


class DetailProviderSerializer(serializers.ModelSerializer):
    logs = ProviderLogSerializer(many=True)

    class Meta:
        model = Provider
        fields = "__all__"


class ProviderSmallDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ("id", "name")
