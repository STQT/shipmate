from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView

from .serializers import *


class ListProviderAPIView(ListAPIView):
    queryset = Provider.objects.all()
    pagination_class = None
    serializer_class = ProviderSmallDataSerializer


class CreateProviderAPIView(CreateAPIView):  # noqa
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

    def perform_create(self, serializer):
        serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)


class UpdateProviderAPIView(UpdateAPIView):
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
