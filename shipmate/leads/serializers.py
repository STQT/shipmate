from django.contrib.auth import get_user_model
from rest_framework import serializers

from shipmate.attachments.models import PhoneAttachment, EmailAttachment, TaskAttachment
from shipmate.attachments.serializers import AttachmentCommentSerializer, NoteAttachmentSerializer, \
    TaskAttachmentSerializer

from shipmate.insights.models import LeadsInsight
from shipmate.contrib.models import Attachments

from shipmate.lead_managements.models import Provider
from shipmate.lead_managements.serializers import ProviderSmallDataSerializer
from shipmate.leads.models import Leads, LeadsAttachment, LeadVehicles
from shipmate.addresses.serializers import CitySerializer
from shipmate.cars.serializers import CarsModelSerializer
from shipmate.customers.serializers import RetrieveCustomerSerializer
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
        lead: Leads = Leads.objects.create(**validated_data)
        leadInsight = LeadsInsight(guid=lead.guid,
                                   status=lead.status,
                                   source=lead.source,
                                   customer=lead.customer,
                                   user=lead.user,
                                   extra_user=lead.extra_user,
                                   updated_at=lead.updated_at)
        leadInsight.save()
        for vehicle_data in vehicles_data:
            LeadVehicles.objects.create(lead=lead, **vehicle_data)

        return lead


class ListLeadMixinSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()  # noqa
    customer_phone = serializers.SerializerMethodField()
    origin_name = serializers.SerializerMethodField()
    destination_name = serializers.SerializerMethodField()
    user = ListUserSerializer(many=False)
    extra_user = ListUserSerializer(many=False, allow_null=True)

    class Meta:
        model = Leads
        fields = "__all__"

    @classmethod
    def get_origin_name(cls, obj) -> str:
        return obj.origin_name

    @classmethod
    def get_destination_name(cls, obj) -> str:
        return obj.destination_name

    @classmethod
    def get_customer_name(cls, obj) -> str:
        return obj.customer_name

    @classmethod
    def get_customer_phone(cls, obj) -> str:
        return obj.customer_phone


class ListLeadsSerializer(ListLeadMixinSerializer):
    lead_vehicles = ListVehicleLeadsSerializer(many=True)
    notes = serializers.SerializerMethodField()  # Add notes field
    tasks = serializers.SerializerMethodField()  # Add tasks field

    class Meta:
        model = Leads
        fields = "__all__"

    def get_notes(self, obj):
        # Filter attachments where type is 'NOTE' and they belong to the lead (obj)
        note_attachments = LeadsAttachment.objects.filter(lead=obj, type=Attachments.TypesChoices.NOTE)
        return LeadsAttachmentSerializer(note_attachments, many=True).data

    def get_tasks(self, obj):
        # Filter tasks related to this lead (obj)
        task_attachments = LeadsAttachment.objects.filter(lead=obj, type=Attachments.TypesChoices.TASK)
        # Serialize the tasks and include deadline_string
        return LeadsAttachmentSerializer(task_attachments, many=True, context=self.context).data


class RetrieveLeadsSerializer(ListLeadsSerializer):
    customer = RetrieveCustomerSerializer(many=False)
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
    user_name = serializers.StringRelatedField(source="user.get_full_name")
    from_phone = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()

    class Meta:
        model = LeadsAttachment
        fields = "__all__"


    def get_from_phone(self, obj: LeadsAttachment):
        if obj.type == Attachments.TypesChoices.PHONE:
            # Assuming `from_phone` is a field in the related order model
            phone = PhoneAttachment.objects.filter(id=obj.link).first()

            return phone.from_phone if phone else None
        else:
            return None


    def get_subject(self, obj: LeadsAttachment):
        if obj.type == Attachments.TypesChoices.EMAIL:
            # Assuming `from_phone` is a field in the related order model
            email = EmailAttachment.objects.filter(id=obj.link).first()

            return email.subject if email else None
        else:
            return None


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
        fields = ["id", "picture", "first_name", "last_name", "count", "is_active"]

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
