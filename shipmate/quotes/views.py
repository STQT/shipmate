from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
    DestroyAPIView, CreateAPIView,
    get_object_or_404, UpdateAPIView, GenericAPIView
)
from rest_framework.mixins import UpdateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .filters import QuoteFilter, QuoteAttachmentFilter
from shipmate.contrib.models import QuoteStatusChoices, Attachments
from shipmate.contrib.generics import RetrieveUpdatePUTDestroyAPIView
from .models import QuoteAttachment, QuoteLog, Quote, QuoteVehicles
from .serializers import (
    ListQuoteSerializer, CreateQuoteSerializer,
    RetrieveQuoteSerializer, UpdateQuoteSerializer,
    VehicleQuoteSerializer, ProviderQuoteListSerializer,
    ListQuoteTeamSerializer, QuoteAttachmentSerializer
)
from ..attachments.models import NoteAttachment, TaskAttachment, FileAttachment
from ..contrib.pagination import CustomPagination
from ..contrib.views import ArchiveView, ReAssignView
from ..customers.models import Customer
from ..insights.models import LeadsInsight
from ..lead_managements.models import Provider
from ..leads.serializers import LogSerializer
from ..leads.views import ListTeamLeadAPIView

VEHICLE_TAG = "quote/vehicle/"
ATTACHMENTS_TAG = "quote/attachments/"
REASON_TAG = "quote/reason/"

User = get_user_model()  # noqa


class QuotePagination(LimitOffsetPagination):
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

    # def get_offset(self, request):
    #
    #     try:
    #         print("BYE")
    #         return _positive_int(
    #             request.query_params[self.offset_query_param],
    #         )
    #     except (KeyError, ValueError):
    #         print("HELLO")
    #         return 1

    def get_offset(self, request):
        """
        Override to set the offset.
        """
        # Get the offset from the request query parameters
        offset = super().get_offset(request)

        # Adjust offset to start from 1 instead of 0
        return max(0, offset - 1)


class ListQuoteAPIView(ListAPIView):  # noqa
    queryset = Quote.objects.prefetch_related(
        "quote_vehicles"
    ).select_related("origin__state", "destination__state", "customer", "user", "extra_user")
    serializer_class = ListQuoteSerializer
    filterset_class = QuoteFilter
    pagination_class = QuotePagination
    ordering = ("-id",)


class CreateQuoteAPIView(CreateAPIView):
    queryset = Quote.objects.all()
    serializer_class = CreateQuoteSerializer

    def perform_create(self, serializer):
        serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)


class UpdateQuoteAPIView(UpdateAPIView):
    queryset = Quote.objects.all()
    serializer_class = UpdateQuoteSerializer
    lookup_field = 'guid'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        original_status = instance.status  # Get the original status


        serializer = self.get_serializer(instance=self.get_object(), data=request.data)
        if serializer.is_valid():
            serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)

            # Check if the status has changed
            new_status = serializer.instance.status
            if original_status != new_status and original_status != 'archived':
                print(f"Moved to {new_status}")  # Log the status change
                QuoteAttachment.objects.create(
                    quote=serializer.instance,
                    type=Attachments.TypesChoices.ACTIVITY,  # Assuming you have types for attachments
                    title=f"Converted to {QuoteStatusChoices(new_status).label}",
                    link=0,
                    user=serializer.instance.user
                )
            elif original_status == 'archived':
                QuoteAttachment.objects.create(
                    quote=serializer.instance,
                    type=Attachments.TypesChoices.ACTIVITY,  # Assuming you have types for attachments
                    title=f"Backed to {QuoteStatusChoices(new_status).label}",
                    link=0,
                    user=serializer.instance.user
                )
            try:
                lead_insight = LeadsInsight.objects.get(quote_guid=serializer.instance.guid)
                lead_insight.status = serializer.instance.status
                lead_insight.source = serializer.instance.source
                lead_insight.price = serializer.instance.price
                lead_insight.reservation_price = serializer.instance.reservation_price
                lead_insight.customer = serializer.instance.customer
                lead_insight.save()
            except Exception as e:
                print(e)

            return Response(RetrieveQuoteSerializer(serializer.instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses={200: RetrieveQuoteSerializer})
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class DeleteQuoteAPIView(DestroyAPIView):
    queryset = Quote.objects.all()
    serializer_class = CreateQuoteSerializer
    lookup_field = 'guid'


class DetailQuoteAPIView(RetrieveAPIView):
    queryset = Quote.objects.prefetch_related(
        Prefetch('quote_vehicles', queryset=QuoteVehicles.objects.order_by('id'))
    )
    serializer_class = RetrieveQuoteSerializer
    lookup_field = 'guid'


@extend_schema(tags=[ATTACHMENTS_TAG])
class QuoteAttachmentListView(UpdateModelMixin, GenericAPIView):
    serializer_class = QuoteAttachmentSerializer
    filterset_class = QuoteAttachmentFilter

    def get_queryset(self):
        quote_id = self.kwargs.get('quoteId')  # Retrieve the lead_id from URL kwargs
        return QuoteAttachment.objects.prefetch_related(
            "quote_attachment_comments").filter(quote_id=quote_id).order_by("-id")


    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # PATCH method to update specific fields of an OrderAttachment
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
class QuoteAttachmentDeleteAPIView(DestroyAPIView):
    serializer_class = QuoteAttachmentSerializer  # noqa

    @transaction.atomic
    def delete(self, request, id):
        quote_attachment = get_object_or_404(QuoteAttachment, id=id)
        quote_attachment.delete()
        model_mapping = {
            'note': NoteAttachment,
            'task': TaskAttachment,
            'file': FileAttachment,
            # Add more mappings as needed
        }
        model_class = model_mapping.get(quote_attachment.type)

        if not model_class:
            raise ValidationError(
                {"type": f"`{quote_attachment.type}` doesn't found from allowed deleting attachment"}
            )

        attachment_instance = model_class.objects.get(id=quote_attachment.link)
        attachment_instance.delete()
        return Response({'message': 'Attachment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class ArchiveListQuoteAPIView(ListAPIView):
    queryset = Quote.objects.filter(status=QuoteStatusChoices.ARCHIVED)
    serializer_class = ListQuoteSerializer


@extend_schema(tags=[VEHICLE_TAG])
class CreateVehicleQuoteAPIView(CreateAPIView):  # noqa
    queryset = QuoteVehicles.objects.all()
    serializer_class = VehicleQuoteSerializer


@extend_schema(tags=[VEHICLE_TAG])
class RetrieveUpdateDestroyVehicleQuoteAPIView(RetrieveUpdatePUTDestroyAPIView):  # noqa
    queryset = QuoteVehicles.objects.all()
    serializer_class = VehicleQuoteSerializer


@extend_schema(parameters=[
    OpenApiParameter(name='status', type=str, location=OpenApiParameter.QUERY,
                     enum=QuoteStatusChoices.values,
                     description='Calculating quoteCount with status', required=True),
])
class ProviderQuoteListAPIView(ListAPIView):
    queryset = Provider.objects.filter(status=Provider.ProviderStatusChoices.ACTIVE)
    pagination_class = None
    serializer_class = ProviderQuoteListSerializer


class ListQuoteLogAPIView(ListAPIView):
    serializer_class = LogSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        quote_id = self.kwargs['quote']
        return QuoteLog.objects.filter(quote_id=quote_id)


@extend_schema(tags=[REASON_TAG])
class ReAssignQuoteView(ReAssignView):
    base_class = Quote
    base_attachment_class = QuoteAttachment
    base_fk_field = "quote"


@extend_schema(tags=[REASON_TAG])
class ArchiveQuoteView(ArchiveView):
    base_class = Quote
    status_choice_class = QuoteStatusChoices
    base_attachment_class = QuoteAttachment
    base_fk_field = "quote"


@extend_schema(parameters=[OpenApiParameter('type', enum=QuoteStatusChoices)])
class ListTeamQuoteAPIView(ListTeamLeadAPIView):
    serializer_class = ListQuoteTeamSerializer
