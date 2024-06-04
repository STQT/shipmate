from rest_framework import generics, viewsets

from .filters import VoIPFilter, MerchantFilter
from .models import CompanyInfo, Merchant, VoIP
from .serializers import CompanyInfoSerializer, MerchantSerializer, VoIPSerializer


class CompanyInfoDetail(generics.RetrieveUpdateAPIView):
    queryset = CompanyInfo.objects.all()  # noqa
    serializer_class = CompanyInfoSerializer

    def perform_create(self, serializer):
        serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)

    def perform_update(self, serializer):
        serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)


class MerchantViewSet(viewsets.ModelViewSet):
    queryset = Merchant.objects.all()  # noqa
    serializer_class = MerchantSerializer
    pagination_class = None
    filterset_class = MerchantFilter

    def perform_create(self, serializer):
        serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)

    def perform_update(self, serializer):
        serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)


class VoIPViewSet(viewsets.ModelViewSet):
    queryset = VoIP.objects.all()  # noqa
    serializer_class = VoIPSerializer
    pagination_class = None
    filterset_class = VoIPFilter

    def perform_create(self, serializer):
        serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)

    def perform_update(self, serializer):
        serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)
