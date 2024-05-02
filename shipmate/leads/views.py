from django.db import transaction, models
from django.db.models import Prefetch, Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
    DestroyAPIView, CreateAPIView,
    UpdateAPIView, RetrieveUpdateDestroyAPIView,
    get_object_or_404
)
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from shipmate.attachments.models import NoteAttachment, TaskAttachment, FileAttachment
from shipmate.lead_managements.models import Provider
from shipmate.leads.filters import LeadsFilter, LeadsAttachmentFilter, LeadsSearchFilter
from shipmate.leads.models import Leads, LeadsAttachment, LeadVehicles
from shipmate.leads.serializers import (
    ListLeadsSerializer,
    CreateLeadsSerializer,
    UpdateLeadsSerializer,
    RetrieveLeadsSerializer,
    LeadsAttachmentSerializer,
    VehicleLeadsSerializer, LeadConvertSerializer, ProviderLeadListSerializer
)
from shipmate.quotes.models import Quote, QuoteVehicles
from shipmate.quotes.serializers import CreateQuoteSerializer


class LeadsPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 1000

    def __init__(self):
        self.sum_price = 0
        self.reservation_price = 0

    def paginate_queryset(self, queryset, request, view=None):
        self.sum_price = queryset.aggregate(
            total_price=models.Sum('price')
        )['total_price'] or 0
        self.reservation_price = queryset.aggregate(
            total_reservation_price=models.Sum('reservation_price')
        )['total_reservation_price'] or 0

        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['sum_price'] = self.sum_price
        response.data['reservation_price'] = self.reservation_price
        return response


class ListLeadsAPIView(ListAPIView):  # noqa
    queryset = Leads.objects.prefetch_related("lead_vehicles")
    serializer_class = ListLeadsSerializer
    filterset_class = LeadsFilter
    pagination_class = LeadsPagination
    ordering = ("-id",)


class LeadsSearchAPIView(ListAPIView):
    serializer_class = ListLeadsSerializer
    pagination_class = LeadsPagination
    filterset_class = LeadsSearchFilter
    queryset = Leads.objects.all().select_related("origin__state", "destination__state", "customer")


class CreateLeadsAPIView(CreateAPIView):  # noqa
    queryset = Leads.objects.all()
    serializer_class = CreateLeadsSerializer


class UpdateLeadsAPIView(UpdateAPIView):
    queryset = Leads.objects.all()
    serializer_class = UpdateLeadsSerializer
    lookup_field = 'guid'


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


class CreateVehicleLeadsAPIView(CreateAPIView):  # noqa
    queryset = LeadVehicles.objects.all()
    serializer_class = VehicleLeadsSerializer


class RetrieveUpdateDestroyVehicleLeadsAPIView(RetrieveUpdateDestroyAPIView):  # noqa
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
            except Leads.DoesNotExist:
                return Response({"error": "Lead not found"}, status=status.HTTP_404_NOT_FOUND)

            lead_data: dict = lead.__dict__
            lead.delete()
            lead_data.pop('_state', None)
            lead_data.pop('id', None)
            lead_data.pop('guid', None)
            lead_data.pop('price', None)
            lead_data.pop('reservation_price', None)
            lead_data.pop('_prefetched_objects_cache', None)

            quote_instance = Quote(price=price, reservation_price=reservation_price, **lead_data)
            quote_instance.save()

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
            quote_serializer = CreateQuoteSerializer(quote_instance)
            return Response(quote_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeadsAttachmentListView(ListAPIView):
    serializer_class = LeadsAttachmentSerializer
    filterset_class = LeadsAttachmentFilter

    def get_queryset(self):
        lead_id = self.kwargs.get('leadId')  # Retrieve the lead_id from URL kwargs
        return LeadsAttachment.objects.filter(lead_id=lead_id).order_by("-id")


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
                     description='Calculating leadsCount with status Leads | Archived'),
])
class ProviderLeadListAPIView(ListAPIView):
    queryset = Provider.objects.filter(is_active=True)
    pagination_class = None
    serializer_class = ProviderLeadListSerializer
