from rest_framework import serializers

from .models import Quote, QuoteVehicles, QuoteAttachment, QuoteDates
from ..addresses.serializers import CitySerializer
from ..attachments.serializers import AttachmentCommentSerializer
from ..cars.serializers import CarsModelSerializer
from ..customers.serializers import CustomerSerializer
from ..lead_managements.models import Provider
from ..lead_managements.serializers import ProviderSmallDataSerializer
from ..leads.serializers import ListLeadUserSerializer, ListLeadTeamSerializer
from ..users.serializers import ListUserSerializer


class CreateVehicleQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteVehicles
        fields = ["vehicle", "vehicle_year"]


class CreateQuoteSerializer(serializers.ModelSerializer):
    vehicles = CreateVehicleQuoteSerializer(many=True, write_only=True)

    class Meta:
        model = Quote
        fields = "__all__"

    def create(self, validated_data):
        vehicles_data = validated_data.pop('vehicles')
        quote = Quote.objects.create(**validated_data)
        for vehicle_data in vehicles_data:
            QuoteVehicles.objects.create(quote=quote, **vehicle_data)
        return quote


class DetailVehicleQuoteSerializer(serializers.ModelSerializer):
    vehicle = CarsModelSerializer(many=False)

    class Meta:
        model = QuoteVehicles
        fields = "__all__"


class QuoteVehicleLeadsSerializer(serializers.ModelSerializer):
    vehicle_name = serializers.SerializerMethodField(read_only=True)  # noqa

    class Meta:
        model = QuoteVehicles
        fields = ["vehicle_name"]

    @classmethod
    def get_vehicle_name(cls, obj) -> str:
        vehicle_mark = "NaN"
        vehicle_name = "NaN"
        if obj.vehicle:
            if obj.vehicle.mark:
                vehicle_mark = obj.vehicle.mark.name
            vehicle_name = obj.vehicle.name
        return f"{obj.vehicle_year} {vehicle_mark} {vehicle_name}"


class ListQuoteSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    customer_phone = serializers.SerializerMethodField()
    origin_name = serializers.SerializerMethodField()
    destination_name = serializers.SerializerMethodField()
    quote_vehicles = QuoteVehicleLeadsSerializer(many=True)
    user = ListUserSerializer(many=False)
    extra_user = ListUserSerializer(many=False, allow_null=True)

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
    def get_customer_name(cls, obj) -> str:
        return obj.customer.name if obj.customer else "NaN"

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


class QuoteDatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteDates
        fields = "__all__"


class RetrieveQuoteSerializer(ListQuoteSerializer):
    customer = CustomerSerializer(many=False)  # noqa
    origin = CitySerializer(many=False)
    destination = CitySerializer(many=False)
    quote_vehicles = DetailVehicleQuoteSerializer(many=True)
    source = ProviderSmallDataSerializer(many=False)
    quote_dates = QuoteDatesSerializer(many=False)

    class Meta:
        model = Quote
        fields = "__all__"


class UpdateQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = "__all__"


class VehicleQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteVehicles
        fields = "__all__"


class ProviderQuoteListSerializer(serializers.ModelSerializer):
    quote_count = serializers.SerializerMethodField()

    def get_quote_count(self, provider) -> int:
        status = self.context['request'].query_params.get('status', None)
        queryset = Quote.objects.filter(source=provider)
        if status:
            queryset = queryset.filter(status=status)
        return queryset.count()

    class Meta:
        model = Provider
        fields = ['id', 'name', 'quote_count']


class QuoteAttachmentSerializer(serializers.ModelSerializer):
    quote_attachment_comments = AttachmentCommentSerializer(many=True, read_only=True)

    class Meta:
        model = QuoteAttachment
        fields = "__all__"


class ListQuoteUserSerializer(ListLeadUserSerializer):
    count = serializers.SerializerMethodField()

    def get_count(self, obj) -> int:
        return Quote.objects.filter(user=obj).count()


class ListQuoteTeamSerializer(ListLeadTeamSerializer):
    users = ListQuoteUserSerializer(many=True)
