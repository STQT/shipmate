from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Prefetch
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
    DestroyAPIView, CreateAPIView,
    get_object_or_404, UpdateAPIView, GenericAPIView
)
from rest_framework import status
from rest_framework.mixins import UpdateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from shipmate.attachments.models import NoteAttachment, TaskAttachment, FileAttachment
from shipmate.contrib.generics import RetrieveUpdatePUTDestroyAPIView
from shipmate.contrib.models import LeadsStatusChoices, QuoteStatusChoices, Attachments
from shipmate.contrib.pagination import CustomPagination
from shipmate.contrib.timetook import timedelta_to_text
from shipmate.contrib.views import ArchiveView, ReAssignView
from shipmate.group_actions.utils import AttachmentType
from shipmate.insights.models import LeadsInsight
from shipmate.lead_managements.models import Provider
from shipmate.leads.filters import LeadsFilter, LeadsAttachmentFilter
from shipmate.leads.models import Leads, LeadsAttachment, LeadVehicles, LeadsLog
from shipmate.leads.serializers import (
    ListLeadsSerializer,
    CreateLeadsSerializer,
    UpdateLeadsSerializer,
    RetrieveLeadsSerializer,
    LeadsAttachmentSerializer,
    VehicleLeadsSerializer,
    LeadConvertSerializer,
    ProviderLeadListSerializer,
    LogSerializer,
    ListLeadTeamSerializer
)
from shipmate.quotes.models import Quote, QuoteVehicles, QuoteAttachment
from shipmate.quotes.serializers import CreateQuoteSerializer
from shipmate.users.models import Team

VEHICLE_TAG = "leads/vehicle/"
ATTACHMENTS_TAG = "leads/attachments/"
REASON_TAG = "leads/reason/"

User = get_user_model()


class LeadsPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 1000

    def get_offset(self, request):
        """
        Override to set the offset.
        """
        # Get the offset from the request query parameters
        offset = super().get_offset(request)

        # Adjust offset to start from 1 instead of 0
        return max(0, offset - 1)


class ListLeadsAPIView(ListAPIView):  # noqa
    queryset = Leads.objects.prefetch_related(
        "lead_vehicles"
    ).select_related("origin__state", "destination__state", "customer", "user", "extra_user")
    serializer_class = ListLeadsSerializer
    filterset_class = LeadsFilter
    pagination_class = LeadsPagination
    ordering = ("-id",)


class CreateLeadsAPIView(CreateAPIView):  # noqa
    queryset = Leads.objects.all()
    serializer_class = CreateLeadsSerializer

    def perform_create(self, serializer):
        serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)


class UpdateLeadsAPIView(UpdateAPIView):
    queryset = Leads.objects.all()
    serializer_class = UpdateLeadsSerializer
    lookup_field = 'guid'

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.get_object(), data=request.data)
        if serializer.is_valid():
            if serializer.instance.status == 'archived':
                LeadsAttachment.objects.create(
                    lead=serializer.instance,
                    type=Attachments.TypesChoices.ACTIVITY,
                    title="Backed to Leads",
                    link=0,
                    user=serializer.instance.user
                )
            serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)
            return Response(RetrieveLeadsSerializer(serializer.instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses={200: RetrieveLeadsSerializer})
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class DeleteLeadsAPIView(DestroyAPIView):
    queryset = Leads.objects.all()
    serializer_class = CreateLeadsSerializer
    lookup_field = 'guid'


class DetailLeadsAPIView(RetrieveAPIView):
    queryset = Leads.objects.prefetch_related(
        Prefetch('lead_vehicles', queryset=LeadVehicles.objects.order_by('id'))
    )
    serializer_class = RetrieveLeadsSerializer
    lookup_field = 'guid'


@extend_schema(tags=[VEHICLE_TAG])
class CreateVehicleLeadsAPIView(CreateAPIView):  # noqa
    queryset = LeadVehicles.objects.all()
    serializer_class = VehicleLeadsSerializer


@extend_schema(tags=[VEHICLE_TAG])
class RetrieveUpdateDestroyVehicleLeadsAPIView(RetrieveUpdatePUTDestroyAPIView):  # noqa
    queryset = LeadVehicles.objects.all()
    serializer_class = VehicleLeadsSerializer


class ConvertLeadToQuoteAPIView(APIView):
    serializer_class = LeadConvertSerializer

    @extend_schema(
        description='Convert lead to quote',
        request=LeadConvertSerializer,
        responses={200: CreateQuoteSerializer(many=False)}
    )
    @transaction.atomic
    def post(self, request, guid):
        serializer = self.serializer_class(data=request.data)

        # Check if the data is valid
        if serializer.is_valid():
            price = serializer.validated_data.get('price')
            reservation_price = serializer.validated_data.get('reservation_price')

            try:
                lead = Leads.objects.prefetch_related("lead_vehicles").get(guid=guid)
                lead_vehicles = lead.lead_vehicles.all()
                # lead_attachments = LeadsAttachment.objects.filter(lead=lead)
            except Leads.DoesNotExist:
                return Response({"error": "Lead not found"}, status=status.HTTP_404_NOT_FOUND)
            # attachment_data = []
            # for attachment in lead_attachments:
            #     one_attachment_data = attachment.__dict__
            #     one_attachment_data.pop('_state', None)
            #     one_attachment_data.pop('id', None)
            #     one_attachment_data.pop('_prefetched_objects_cache', None)
            #     one_attachment = {
            #         "attachment": one_attachment_data,
            #         "comments": []
            #     }
            #     all_comments = LeadAttachmentComment.objects.filter(attachment=attachment)
            #     print(type(all_comments))
            #     for comment in all_comments:
            #         one_attachment['comments'].append(comment.text)
            #     # attachment_data.append(
            #     #     one_attachment
            #     # )
            lead_data: dict = lead.__dict__
            lead_guid = lead.guid
            lead.delete()
            lead_data.pop('_state', None)
            lead_data.pop('id', None)
            lead_data.pop('guid', None)
            lead_data.pop('price', None)
            lead_data.pop('reservation_price', None)
            lead_data.pop('_prefetched_objects_cache', None)
            lead_data['status'] = QuoteStatusChoices.QUOTES


            quote_instance = Quote(price=price, reservation_price=reservation_price, **lead_data)
            quote_instance.save()
            quote_dates = quote_instance.quote_dates
            quote_dates.received = lead_data['created_at']
            quote_dates.created = timezone.now()
            quote_dates.quoted = timezone.now()
            quote_dates.converted = timezone.now()
            quote_dates.save()

            try:
                lead_insight = LeadsInsight.objects.get(guid=lead_guid)
                lead_insight.price = price
                lead_insight.reservation_price = reservation_price
                lead_insight.status = QuoteStatusChoices.QUOTES
                lead_insight.quote_guid = quote_instance.guid
                lead_insight.save()
            except Exception as e:
                print('not found ', e)

            if lead_vehicles:
                quote_vehicles = [
                    QuoteVehicles(
                        quote=quote_instance,
                        vehicle=lead_vehicle.vehicle,
                        vehicle_year=lead_vehicle.vehicle_year
                    )
                    for lead_vehicle in lead_vehicles
                ]
                QuoteVehicles.objects.bulk_create(quote_vehicles)
            # if lead_attachments:
            #     quote_attachments = [
            #         QuoteAttachment(
            #             quote=quote_instance,
            #
            #         )
            #         for lead_attachment in lead_attachments_data
            #     ]
            user = User.objects.get(id=request.user.id)
            time_took = timezone.now() - lead_data['created_at']
            QuoteAttachment.objects.create(
                quote=quote_instance,
                type=Attachments.TypesChoices.ACTIVITY,  # Assuming you have types for attachments
                title="Converted to quote",
                link=0,
                user=user,
                time_took=timedelta_to_text(time_took)
            )
            quote_serializer = CreateQuoteSerializer(quote_instance)
            return Response(quote_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=[ATTACHMENTS_TAG])
class LeadsAttachmentListView(UpdateModelMixin, GenericAPIView):
    serializer_class = LeadsAttachmentSerializer
    filterset_class = LeadsAttachmentFilter

    def get_queryset(self):
        lead_id = self.kwargs.get('leadId')  # Retrieve the lead_id from URL kwargs
        return LeadsAttachment.objects.prefetch_related(
            "lead_attachment_comments").filter(lead_id=lead_id).order_by("-id")


# List method (same as before for GET)
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # PATCH method to update specific fields of a LeadsAttachment
    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # Ensure it's a partial update

        # Extract attachment_id from query parameters
        attachment_id = request.query_params.get('attachment_id')

        if not attachment_id:
            return Response({"detail": "attachment_id parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset()  # Get the queryset filtered by lead_id
        attachment = queryset.filter(pk=attachment_id).first()  # Filter using attachment_id

        if not attachment:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(attachment, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


@extend_schema(tags=[ATTACHMENTS_TAG])
class AttachmentDeleteAPIView(DestroyAPIView):
    serializer_class = LeadsAttachmentSerializer

    @transaction.atomic
    def delete(self, request, id):
        lead_attachment = get_object_or_404(LeadsAttachment, id=id)
        lead_attachment.delete()
        model_mapping = {
            'note': NoteAttachment,
            'task': TaskAttachment,
            'file': FileAttachment,
            # Add more mappings as needed
        }
        model_class = model_mapping.get(lead_attachment.type)

        if not model_class:
            raise ValidationError({"type": f"`{lead_attachment.type}` doesn't found from allowed deleting attachment"})

        attachment_instance = model_class.objects.get(id=lead_attachment.link)
        attachment_instance.delete()
        return Response({'message': 'Attachment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@extend_schema(parameters=[
    OpenApiParameter(name='status', type=str, location=OpenApiParameter.QUERY,
                     enum=LeadsStatusChoices.values,
                     description='Calculating leadsCount with status leads | archived', required=True),
])
class ProviderLeadListAPIView(ListAPIView):
    queryset = Provider.objects.filter(status=Provider.ProviderStatusChoices.ACTIVE)
    pagination_class = None
    serializer_class = ProviderLeadListSerializer


class ListLeadLogAPIView(ListAPIView):
    serializer_class = LogSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        lead_id = self.kwargs['lead']
        return LeadsLog.objects.filter(lead_id=lead_id)


@extend_schema(parameters=[OpenApiParameter('type', enum=LeadsStatusChoices)])
class ListTeamLeadAPIView(ListAPIView):
    serializer_class = ListLeadTeamSerializer
    pagination_class = None

    def get_queryset(self):
        return Team.objects.all().prefetch_related(
            Prefetch('users', queryset=User.objects.all())
        )
        # return Team.objects.filter(status=Team.TeamStatusChoices.ACTIVE).prefetch_related(
        #     Prefetch('users', queryset=User.objects.filter(is_active=True))
        # )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['type'] = self.request.query_params.get('type')
        return context


@extend_schema(tags=[REASON_TAG])
class ReAssignLeadView(ReAssignView):
    pass


@extend_schema(tags=[REASON_TAG])
class ArchiveLeadView(ArchiveView):
    pass
