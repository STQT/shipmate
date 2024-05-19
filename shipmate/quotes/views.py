from django.db import models
from django.db.models import Prefetch
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView
from rest_framework.pagination import LimitOffsetPagination

from .filters import QuoteFilter
from shipmate.quotes.serializers import *
from shipmate.contrib.models import QuoteStatusChoices
from shipmate.contrib.generics import UpdatePUTAPIView


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


class ArchiveListQuoteAPIView(ListAPIView):
    queryset = Quote.objects.filter(status=QuoteStatusChoices.ARCHIVED)
    serializer_class = ListQuoteSerializer
