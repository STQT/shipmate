from django.db import models, transaction
from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView, get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .filters import QuoteFilter, QuoteAttachmentFilter
from shipmate.quotes.serializers import *
from shipmate.contrib.models import QuoteStatusChoices
from shipmate.contrib.generics import UpdatePUTAPIView, RetrieveUpdatePUTDestroyAPIView
from .models import QuoteAttachment, QuoteLog
from ..attachments.models import NoteAttachment, TaskAttachment, FileAttachment
from ..contrib.pagination import CustomPagination
from ..lead_managements.models import Provider
from ..leads.serializers import LogSerializer

VEHICLE_TAG = "quote/vehicle/"
ATTACHMENTS_TAG = "quote/attachments/"


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


class UpdateQuoteAPIView(UpdatePUTAPIView):
    queryset = Quote.objects.all()
    serializer_class = UpdateQuoteSerializer
    lookup_field = 'guid'

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.get_object(), data=request.data)
        if serializer.is_valid():
            serializer.save()
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
class QuoteAttachmentListView(ListAPIView):
    serializer_class = QuoteAttachmentSerializer
    filterset_class = QuoteAttachmentFilter

    def get_queryset(self):
        lead_id = self.kwargs.get('quoteId')  # Retrieve the lead_id from URL kwargs
        return QuoteAttachment.objects.filter(quote_id=lead_id).order_by("-id")


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
            raise ValidationError({"type": f"`{quote_attachment.type}` doesn't found from allowed deleting attachment"})

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
