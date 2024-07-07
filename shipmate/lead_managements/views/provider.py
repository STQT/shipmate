from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView

from shipmate.lead_managements.filters import ProviderFilter
from shipmate.contrib.generics import UpdatePUTAPIView
from shipmate.lead_managements.models import Provider
from shipmate.lead_managements.serializers import (
    ProviderSerializer,
    DetailProviderSerializer,
    CreateProviderSerializer
)


class ListProviderAPIView(ListAPIView):
    queryset = Provider.objects.all()
    pagination_class = None
    serializer_class = ProviderSerializer
    filterset_class = ProviderFilter


class CreateProviderAPIView(CreateAPIView):  # noqa
    queryset = Provider.objects.all()
    serializer_class = CreateProviderSerializer

    def perform_create(self, serializer):
        serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)


class UpdateProviderAPIView(UpdatePUTAPIView):
    queryset = Provider.objects.all()
    serializer_class = CreateProviderSerializer

    def perform_update(self, serializer):
        serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)


class DeleteProviderAPIView(DestroyAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class DetailProviderAPIView(RetrieveAPIView):
    queryset = Provider.objects.prefetch_related("logs")
    serializer_class = DetailProviderSerializer
