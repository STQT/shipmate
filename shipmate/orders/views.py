from django.db import models
from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView
from rest_framework.pagination import LimitOffsetPagination

from .filters import OrderFilter
from shipmate.orders.serializers import *
from shipmate.contrib.models import OrderStatusChoices
from shipmate.contrib.generics import UpdatePUTAPIView, RetrieveUpdatePUTDestroyAPIView
from .models import Order


VEHICLE_TAG = "orders/vehicle/"

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
    queryset = Provider.objects.filter(is_active=True)
    pagination_class = None
    serializer_class = ProviderOrderListSerializer
