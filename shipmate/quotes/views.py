from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView

from .serializers import *


class ListQuoteAPIView(ListAPIView):
    queryset = Quote.objects.all()
    serializer_class = ListQuoteSerializer


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
