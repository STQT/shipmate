from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView

from .filters import QuoteFilter
from shipmate.quotes.serializers import *
from shipmate.contrib.models import QuoteStatusChoices
from shipmate.contrib.generics import UpdatePUTAPIView


class ListQuoteAPIView(ListAPIView):  # noqa
    queryset = Quote.objects.all()
    serializer_class = ListQuoteSerializer
    filterset_class = QuoteFilter
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
    queryset = Quote.objects.all()
    serializer_class = RetrieveQuoteSerializer
    lookup_field = 'guid'


class ArchiveListQuoteAPIView(ListAPIView):
    queryset = Quote.objects.filter(status=QuoteStatusChoices.ARCHIVED)
    serializer_class = ListQuoteSerializer
