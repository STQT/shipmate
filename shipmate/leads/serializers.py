from rest_framework import serializers

from .models import Leads


class CreateLeadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leads
        fields = "__all__"


class ListLeadsSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name')
    customer_phone = serializers.CharField(source='customer.phone')
    origin_name = serializers.SerializerMethodField()
    destination_name = serializers.SerializerMethodField()
    vehicle_name = serializers.SerializerMethodField()

    class Meta:
        model = Leads
        fields = "__all__"

    @classmethod
    def get_origin_name(cls, obj):
        return f"{obj.origin.state.name}, {obj.origin.state.code} {obj.origin.zip}"

    @classmethod
    def get_destination_name(cls, obj):
        return f"{obj.destination.state.name}, {obj.destination.state.code} {obj.destination.zip}"

    @classmethod
    def get_vehicle_name(cls, obj):
        return f"{obj.vehicle_year} {obj.vehicle.mark.name} {obj.vehicle.name}"


class RetrieveLeadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leads
        fields = "__all__"


class UpdateLeadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leads
        fields = "__all__"
