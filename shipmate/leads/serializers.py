from django.contrib.auth import get_user_model
from rest_framework import serializers

from shipmate.attachments.serializers import AttachmentCommentSerializer
from shipmate.lead_managements.models import Provider
from shipmate.lead_managements.serializers import ProviderSmallDataSerializer
from shipmate.leads.models import Leads, LeadsAttachment, LeadVehicles
from shipmate.addresses.serializers import CitySerializer
from shipmate.cars.serializers import CarsModelSerializer
from shipmate.customers.serializers import CustomerSerializer
from shipmate.users.models import Team
from shipmate.users.serializers import ListUserSerializer

User = get_user_model()


class VehicleLeadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadVehicles
        fields = "__all__"


class ListVehicleLeadsSerializer(serializers.ModelSerializer):
    vehicle_name = serializers.SerializerMethodField(read_only=True)  # noqa

    class Meta:
        model = LeadVehicles
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


class DetailVehicleLeadsSerializer(serializers.ModelSerializer):
    vehicle = CarsModelSerializer(many=False)

    class Meta:
        model = LeadVehicles
        fields = "__all__"


class CreateVehicleLeadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadVehicles
        fields = ["vehicle", "vehicle_year"]


class CreateLeadsSerializer(serializers.ModelSerializer):
    vehicles = CreateVehicleLeadsSerializer(many=True, write_only=True)

    class Meta:
        model = Leads
        exclude = ["price", "reservation_price"]

    def create(self, validated_data):
        vehicles_data = validated_data.pop('vehicles')
        lead = Leads.objects.create(**validated_data)
        for vehicle_data in vehicles_data:
            LeadVehicles.objects.create(lead=lead, **vehicle_data)
        return lead


class ListLeadsSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()  # noqa
    customer_phone = serializers.SerializerMethodField()
    origin_name = serializers.SerializerMethodField()
    destination_name = serializers.SerializerMethodField()
    lead_vehicles = ListVehicleLeadsSerializer(many=True)
    user = ListUserSerializer(many=False)
    extra_user = ListUserSerializer(many=False, allow_null=True)

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


class RetrieveLeadsSerializer(ListLeadsSerializer):
    customer = CustomerSerializer(many=False)
    origin = CitySerializer(many=False)
    destination = CitySerializer(many=False)
    lead_vehicles = DetailVehicleLeadsSerializer(many=True)
    source = ProviderSmallDataSerializer(many=False)

    class Meta:
        model = Leads
        fields = "__all__"


class UpdateLeadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leads
        fields = "__all__"


class LeadsAttachmentSerializer(serializers.ModelSerializer):
    lead_attachment_comments = AttachmentCommentSerializer(many=True, read_only=True)

    class Meta:
        model = LeadsAttachment
        fields = "__all__"


class LeadConvertSerializer(serializers.Serializer):
    price = serializers.IntegerField(write_only=True)
    reservation_price = serializers.IntegerField(write_only=True)
    quote = serializers.BooleanField()
    # TODO: if quote True send to quote email


class ProviderLeadListSerializer(serializers.ModelSerializer):
    lead_count = serializers.SerializerMethodField()

    def get_lead_count(self, provider) -> int:
        status = self.context['request'].query_params.get('status', None)
        queryset = Leads.objects.filter(source=provider)
        if status:
            queryset = queryset.filter(status=status)
        return queryset.count()

    class Meta:
        model = Provider
        fields = ['id', 'name', 'lead_count']


class LogSerializer(serializers.Serializer):
    title = serializers.CharField()
    message = serializers.CharField(allow_null=True)


class ListLeadUserSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "picture", "first_name", "last_name", "count"]

    def get_count(self, obj) -> int:
        status = self.context.get('type')
        if status:
            return Leads.objects.filter(user=obj, status=status).count()
        return Leads.objects.filter(user=obj).count()


class ListLeadTeamSerializer(serializers.ModelSerializer):
    users = ListLeadUserSerializer(many=True)

    class Meta:
        model = Team
        fields = ["name", "users"]
