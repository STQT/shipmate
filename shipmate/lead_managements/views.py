from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView

from .serializers import *


class ListProviderAPIView(ListAPIView):
    queryset = Provider.objects.all()
    pagination_class = None
    serializer_class = ProviderSmallDataSerializer


class CreateProviderAPIView(CreateAPIView):  # noqa
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class UpdateProviderAPIView(UpdateAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class DeleteProviderAPIView(DestroyAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class DetailProviderAPIView(RetrieveAPIView):
    queryset = Provider.objects.prefetch_related("logs")
    serializer_class = DetailProviderSerializer
