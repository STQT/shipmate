from rest_framework import serializers

from .models import Quote
from ..leads.serializers import DetailVehicleLeadsSerializer


class CreateQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = "__all__"


class ListQuoteSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name')
    customer_phone = serializers.CharField(source='customer.phone')
    origin_name = serializers.SerializerMethodField()
    destination_name = serializers.SerializerMethodField()
    quote_vehicles = DetailVehicleLeadsSerializer(many=True)

    class Meta:
        model = Quote
        fields = "__all__"

    @classmethod
    def get_origin_name(cls, obj) -> str:
        city_name = "NaN"  # noqa
        state_code = "NaN"
        city_zip = "NaN"

        if obj.origin:
            if obj.origin.state:
                city_name = obj.origin.name
                state_code = obj.origin.state.code
            city_zip = obj.origin.zip

        return f"{city_name}, {state_code} {city_zip}"

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


class RetrieveQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = "__all__"


class UpdateQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = "__all__"
