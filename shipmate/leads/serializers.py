from rest_framework import serializers

from shipmate.lead_managements.serializers import ProviderSmallDataSerializer
from shipmate.leads.models import Leads, LeadsAttachment
from shipmate.addresses.serializers import CitySerializer
from shipmate.cars.serializers import CarsModelSerializer
from shipmate.customers.serializers import CustomerSerializer


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
    def get_origin_name(cls, obj) -> str:
        state_name = "NaN"  # noqa
        state_code = "NaN"
        city_zip = "NaN"

        if obj.origin:
            if obj.origin.state:
                state_name = obj.origin.state.name
                state_code = obj.origin.state.code
            city_zip = obj.origin.zip

        return f"{state_name}, {state_code} {city_zip}"

    @classmethod
    def get_destination_name(cls, obj) -> str:
        state_name = "NaN"  # noqa
        state_code = "NaN"
        city_zip = "NaN"

        if obj.destination:
            if obj.destination.state:
                state_name = obj.destination.state.name
                state_code = obj.destination.state.code
            city_zip = obj.destination.zip

        return f"{state_name}, {state_code} {city_zip}"

    @classmethod
    def get_vehicle_name(cls, obj) -> str:
        vehicle_mark = "NaN"
        vehicle_name = "NaN"
        if obj.vehicle:
            if obj.vehicle.mark:
                vehicle_mark = obj.vehicle.mark.name
            vehicle_name = obj.vehicle.name
        return f"{obj.vehicle_year} {vehicle_mark} {vehicle_name}"


class RetrieveLeadsSerializer(ListLeadsSerializer):
    customer = CustomerSerializer(many=False)
    origin = CitySerializer(many=False)
    destination = CitySerializer(many=False)
    vehicle = CarsModelSerializer(many=False)
    source = ProviderSmallDataSerializer(many=False)

    class Meta:
        model = Leads
        fields = "__all__"


class UpdateLeadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leads
        fields = "__all__"


class LeadsAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadsAttachment
        fields = "__all__"
