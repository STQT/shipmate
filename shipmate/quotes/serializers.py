from rest_framework import serializers

from .models import Quote, QuoteVehicles, QuoteAttachment, QuoteDates
from ..addresses.serializers import CitySerializer
from ..attachments.models import PhoneAttachment, EmailAttachment
from ..attachments.serializers import AttachmentCommentSerializer
from ..cars.serializers import CarsModelSerializer
from ..contrib.models import Attachments
from ..customers.serializers import RetrieveCustomerSerializer
from ..lead_managements.models import Provider
from ..lead_managements.serializers import ProviderSmallDataSerializer
from ..leads.serializers import ListLeadUserSerializer, ListLeadTeamSerializer, ListLeadMixinSerializer
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


class QuoteDatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteDates
        fields = "__all__"


class ListQuoteSerializer(ListLeadMixinSerializer):
    quote_vehicles = QuoteVehicleLeadsSerializer(many=True)
    quote_dates = QuoteDatesSerializer(many=False)
    notes = serializers.SerializerMethodField()  # Add notes field


    class Meta:
        model = Quote
        fields = "__all__"

    def get_notes(self, obj):
        # Filter attachments where type is 'NOTE' and they belong to the lead (obj)
        note_attachments = QuoteAttachment.objects.filter(quote=obj, type=Attachments.TypesChoices.NOTE)
        return QuoteAttachmentSerializer(note_attachments, many=True).data


class RetrieveQuoteSerializer(ListQuoteSerializer):
    customer = RetrieveCustomerSerializer(many=False)  # noqa
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
    user_name = serializers.StringRelatedField(source="user.get_full_name")
    from_phone = serializers.SerializerMethodField()
    filename = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()


    class Meta:
        model = QuoteAttachment
        fields = "__all__"

    def get_from_phone(self, obj: QuoteAttachment):
        if obj.type == Attachments.TypesChoices.PHONE:
            # Assuming `from_phone` is a field in the related order model
            phone = PhoneAttachment.objects.filter(id=obj.link).first()
            return phone.from_phone if phone else None
        else:
            return None


    def get_filename(self, obj: QuoteAttachment):
        if obj.type == Attachments.TypesChoices.FILE:
            try:
                return obj.file.split('/')[-1] # noqa
            except Exception as e:
                print(e)
                return 'some error'
        else:
            return None

    def get_subject(self, obj: QuoteAttachment):
        if obj.type == Attachments.TypesChoices.EMAIL:
            # Assuming `from_phone` is a field in the related order model
            email = EmailAttachment.objects.filter(id=obj.link).first()

            return email.subject if email else None
        else:
            return None


class ListQuoteUserSerializer(ListLeadUserSerializer):
    count = serializers.SerializerMethodField()

    def get_count(self, obj) -> int:
        status = self.context.get('type')
        if status:
            return Quote.objects.filter(user=obj, status=status).count()
        return Quote.objects.filter(user=obj).count()


class ListQuoteTeamSerializer(ListLeadTeamSerializer):
    users = ListQuoteUserSerializer(many=True)
