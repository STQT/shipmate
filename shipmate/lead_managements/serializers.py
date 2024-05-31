from rest_framework import serializers

from shipmate.lead_managements.models import Distribution, DistributionLog, Provider, ProviderLog


class ProviderLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderLog
        fields = ("title", "message")


class ProviderSerializer(serializers.ModelSerializer):
    updated_from_email = serializers.StringRelatedField(source="updated_from.email", read_only=True)

    class Meta:
        model = Provider
        fields = "__all__"


class DetailProviderSerializer(serializers.ModelSerializer):
    logs = ProviderLogSerializer(many=True)
    updated_from_email = serializers.StringRelatedField(source="updated_from.email", read_only=True)

    class Meta:
        model = Provider
        fields = "__all__"


class ProviderSmallDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ("id", "name")


class DistributionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistributionLog
        fields = ("title", "message")


class UpdateDistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distribution
        exclude = ("user", "updated_from")


class ListDistributionSerializer(serializers.ModelSerializer):
    user_email = serializers.StringRelatedField(source="user.email")
    updated_from_email = serializers.StringRelatedField(source="updated_from.email")
    # TODO: update to dynamic
    received_today = serializers.IntegerField(default=1, allow_null=True, read_only=True)
    queue_now = serializers.IntegerField(default=1, allow_null=True, read_only=True)

    class Meta:
        model = Distribution
        fields = "__all__"


class DetailDistributionSerializer(ListDistributionSerializer):
    logs = DistributionLogSerializer(many=True)

    # TODO: Add fields received_today and queue now

    class Meta:
        model = Distribution
        fields = "__all__"


class DistributionSmallDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distribution
        fields = "__all__"
