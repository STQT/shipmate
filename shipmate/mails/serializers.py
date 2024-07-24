from rest_framework import serializers

from shipmate.contrib.models import TrailerTypeChoices
from shipmate.leads.models import Leads
from shipmate.leads.serializers import ListVehicleLeadsSerializer
from shipmate.users.serializers import ListUserSerializer


class DataListSerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.CharField()


class BlockListSerializer(serializers.Serializer):
    blockName = serializers.CharField()
    data = DataListSerializer(many=True)


class ModulesListSerializer(serializers.Serializer):
    title = serializers.CharField()
    block = BlockListSerializer(many=True)


class StringListField(serializers.ListField):
    child = serializers.CharField()


class CDPriceSerializer(serializers.Serializer):
    cargo = StringListField(read_only=True)
    route = StringListField(read_only=True)
    price = StringListField(read_only=True)
    accepted = StringListField(read_only=True)
    comparable = StringListField(read_only=True)
    title = serializers.CharField(read_only=True)


class CDPOSTPriceSerializer(CDPriceSerializer):
    origin_zip = serializers.CharField(max_length=5, write_only=True, required=True)
    destination_zip = serializers.CharField(max_length=5, write_only=True, required=True)
    trailer_type = serializers.ChoiceField(required=True, choices=TrailerTypeChoices.choices,
                                           write_only=True, help_text="Trailer tipi")
    vehicle_type = serializers.CharField(write_only=True, required=True, help_text="Vehicle tipi")
    vehicles_length = serializers.IntegerField(default=1, help_text="Vehicle larni soni")


class GlobalListLeadsSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()  # noqa
    customer_phone = serializers.SerializerMethodField()
    origin_name = serializers.SerializerMethodField()
    destination_name = serializers.SerializerMethodField()
    vehicles = serializers.SerializerMethodField()
    user = ListUserSerializer(many=False)
    extra_user = ListUserSerializer(many=False, allow_null=True)
    status_type = serializers.CharField()

    class Meta:
        model = Leads
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
    def get_customer_name(cls, obj) -> str:
        customer = obj.customer
        if not obj.customer:
            return "NaN"
        name = customer.name
        last_name = customer.last_name if customer.last_name else ""
        return name + " " + last_name

    @classmethod
    def get_customer_phone(cls, obj) -> str:
        return obj.customer.phone if obj.customer else "NaN"

    @classmethod
    def get_destination_name(cls, obj) -> str:
        city_name = "NaN"  # noqa
        state_code = "NaN"
        city_zip = "NaN"

        if obj.destination:
            if obj.destination.state:
                city_name = obj.destination.name
                state_code = obj.destination.state.code
            city_zip = obj.destination.zip

        return f"{city_name}, {state_code} {city_zip}"

    def get_vehicles(self, obj) -> ListVehicleLeadsSerializer(many=True):
        if obj.status_type == "Quotes":
            return ListVehicleLeadsSerializer(obj.quote_vehicles.all(), many=True).data
        elif obj.status_type == "Orders":
            return ListVehicleLeadsSerializer(obj.order_vehicles.all(), many=True).data
        return ListVehicleLeadsSerializer(obj.lead_vehicles.all(), many=True).data


class GlobalSearchSerializer(serializers.Serializer):
    data = GlobalListLeadsSerializer(many=True, allow_empty=True)


class GlobalSearchIDSerializer(serializers.Serializer):
    leads = serializers.BooleanField()
    quotes = serializers.BooleanField()
    orders = serializers.BooleanField()
