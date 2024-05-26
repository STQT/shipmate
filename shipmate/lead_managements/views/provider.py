from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView

from shipmate.lead_managements.serializers import *
from shipmate.contrib.generics import UpdatePUTAPIView


class ListProviderAPIView(ListAPIView):
    queryset = Provider.objects.filter(is_active=True)
    pagination_class = None
    serializer_class = ProviderSmallDataSerializer


class CreateProviderAPIView(CreateAPIView):  # noqa
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

    def perform_create(self, serializer):
        serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)


class UpdateProviderAPIView(UpdatePUTAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

    def perform_update(self, serializer):
        serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)


class DeleteProviderAPIView(DestroyAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class DetailProviderAPIView(RetrieveAPIView):
    queryset = Provider.objects.prefetch_related("logs")
    serializer_class = DetailProviderSerializer
