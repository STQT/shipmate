from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView

from .filters import QuoteFilter
from .serializers import *
from ..contrib.models import QuoteStatusChoices


class ListQuoteAPIView(ListAPIView):
    queryset = Quote.objects.all()
    serializer_class = ListQuoteSerializer
    filterset_class = QuoteFilter
    ordering_fields = ['updated_at', 'id', 'customer', 'phone', 'vehicle', 'origin', 'destination', 'date_est_ship']


class CreateQuoteAPIView(CreateAPIView):
    queryset = Quote.objects.all()
    serializer_class = CreateQuoteSerializer


class UpdateQuoteAPIView(UpdateAPIView):
    queryset = Quote.objects.all()
    serializer_class = UpdateQuoteSerializer


class DeleteQuoteAPIView(DestroyAPIView):
    queryset = Quote.objects.all()
    serializer_class = CreateQuoteSerializer


class DetailQuoteAPIView(RetrieveAPIView):
    queryset = Quote.objects.all()
    serializer_class = RetrieveQuoteSerializer


class ArchiveListQuoteAPIView(ListAPIView):
    queryset = Quote.objects.filter(status=QuoteStatusChoices.ARCHIVED)
    serializer_class = ListQuoteSerializer
