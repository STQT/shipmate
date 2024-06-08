from django.db import models, transaction
from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView, get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .filters import OrderFilter, OrderAttachmentFilter
from shipmate.orders.serializers import *
from shipmate.contrib.models import OrderStatusChoices
from shipmate.contrib.generics import UpdatePUTAPIView, RetrieveUpdatePUTDestroyAPIView
from .models import Order, OrderAttachment, OrderLog
from ..attachments.models import NoteAttachment, TaskAttachment, FileAttachment
from ..contrib.pagination import CustomPagination
from ..leads.serializers import LogSerializer
from ..quotes.models import Quote
from ..quotes.serializers import CreateQuoteSerializer

VEHICLE_TAG = "orders/vehicle/"
ATTACHMENTS_TAG = "orders/attachments/"


class OrderPagination(LimitOffsetPagination):
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


class ListOrderAPIView(ListAPIView):  # noqa
    queryset = Order.objects.prefetch_related(
        "order_vehicles"
    ).select_related("origin__state", "destination__state", "customer", "user", "extra_user")
    serializer_class = ListOrderSerializer
    filterset_class = OrderFilter
    pagination_class = OrderPagination
    ordering = ("-id",)


class CreateOrderAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer


class UpdateOrderAPIView(UpdatePUTAPIView):
    queryset = Order.objects.all()
    serializer_class = UpdateOrderSerializer
    lookup_field = 'guid'

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.get_object(), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(RetrieveOrderSerializer(serializer.instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses={200: RetrieveOrderSerializer})
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)


class DeleteOrderAPIView(DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer
    lookup_field = 'guid'


class DetailOrderAPIView(RetrieveAPIView):
    queryset = Order.objects.prefetch_related(
        Prefetch('order_vehicles', queryset=OrderVehicles.objects.order_by('id'))
    )
    serializer_class = RetrieveOrderSerializer
    lookup_field = 'guid'


class ArchiveListOrderAPIView(ListAPIView):
    queryset = Order.objects.filter(status=OrderStatusChoices.ARCHIVED)
    serializer_class = ListOrderSerializer


@extend_schema(tags=[ATTACHMENTS_TAG])
class OrderAttachmentListView(ListAPIView):
    serializer_class = OrderAttachmentSerializer
    filterset_class = OrderAttachmentFilter

    def get_queryset(self):
        lead_id = self.kwargs.get('ordersId')  # Retrieve the lead_id from URL kwargs
        return OrderAttachment.objects.filter(order_id=lead_id).order_by("-id")


@extend_schema(tags=[ATTACHMENTS_TAG])
class OrderAttachmentDeleteAPIView(DestroyAPIView):
    serializer_class = OrderAttachmentSerializer  # noqa

    @transaction.atomic
    def delete(self, request, id):
        order_attachment = get_object_or_404(OrderAttachment, id=id)
        order_attachment.delete()
        model_mapping = {
            'note': NoteAttachment,
            'task': TaskAttachment,
            'file': FileAttachment,
            # Add more mappings as needed
        }
        model_class = model_mapping.get(order_attachment.type)

        if not model_class:
            raise ValidationError({"type": f"`{order_attachment.type}` doesn't found from allowed deleting attachment"})

        attachment_instance = model_class.objects.get(id=order_attachment.link)
        attachment_instance.delete()
        return Response({'message': 'Attachment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=[VEHICLE_TAG])
class CreateVehicleOrderAPIView(CreateAPIView):  # noqa
    queryset = OrderVehicles.objects.all()
    serializer_class = VehicleOrderSerializer


@extend_schema(tags=[VEHICLE_TAG])
class RetrieveUpdateDestroyVehicleOrderAPIView(RetrieveUpdatePUTDestroyAPIView):  # noqa
    queryset = OrderVehicles.objects.all()
    serializer_class = VehicleOrderSerializer


@extend_schema(parameters=[
    OpenApiParameter(name='status', type=str, location=OpenApiParameter.QUERY,
                     enum=OrderStatusChoices.values,
                     description='Calculating leadsCount with status', required=True),
])
class ProviderOrderListAPIView(ListAPIView):
    queryset = Provider.objects.filter(status=Provider.ProviderStatusChoices.ACTIVE)
    pagination_class = None
    serializer_class = ProviderOrderListSerializer


class DispatchingOrderCreateAPIView(UpdatePUTAPIView):
    queryset = Order.objects.all()
    serializer_class = DispatchingOrderSerializer
    lookup_field = "guid"

    def perform_update(self, serializer):
        serializer.save(status=OrderStatusChoices.DISPATCHED)


class DirectDispatchOrderCreateAPIView(UpdatePUTAPIView):
    queryset = Order.objects.all()
    serializer_class = DirectDispatchOrderSerializer
    lookup_field = "guid"

    def perform_update(self, serializer):
        serializer.save(
            status=OrderStatusChoices.DISPATCHED,
            updated_from=self.request.user if self.request.user.is_authenticated else None
        )


class ListOrderLogAPIView(ListAPIView):
    serializer_class = LogSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        order_id = self.kwargs['order']
        return OrderLog.objects.filter(order_id=order_id)


class ConvertQuoteToOrderAPIView(CreateAPIView):
    serializer_class = CreateOrderSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        quote_id = self.kwargs.get('quote')
        quote = get_object_or_404(Quote, id=quote_id)
        serializer.save()
        quote.delete()


class BackToQuoteOrderAPIView(CreateAPIView):
    serializer_class = None

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer_class = CreateQuoteSerializer
        order_id = self.kwargs.get('order')
        order = get_object_or_404(Order, id=order_id)
        quote_data = {
            'origin': order.origin.pk,
            'destination': order.destination.pk,
            'user': order.user.pk,
            'extra_user': order.extra_user.pk if order.extra_user else None,
            'updated_from': request.user.pk if request.user.is_authenticated else None,
            'source': order.source.pk if order.source else None,
            'customer': order.customer.pk if order.customer else None
        }
        order_data = order.__dict__
        order_data['vehicles'] = []
        for order_vehicle in order.order_vehicles.all():  # noqa
            order_data['vehicles'].append(
                {"vehicle": order_vehicle.vehicle.pk, "vehicle_year": order_vehicle.vehicle_year}
            )
        order_data['status'] = 'quote'
        order_data.update(quote_data)
        quote_serializer = serializer_class(data=order_data)
        quote_serializer.is_valid(raise_exception=True)
        quote_serializer.save()

        order.delete()

        return Response(quote_serializer.data, status=status.HTTP_201_CREATED)
