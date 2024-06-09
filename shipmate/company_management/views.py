from rest_framework import generics, viewsets

from .filters import VoIPFilter, MerchantFilter, TemplateFilter, PaymentAppFilter
from .models import CompanyInfo, Merchant, VoIP, Template, PaymentApp
from .serializers import CompanyInfoSerializer, MerchantSerializer, VoIPSerializer, TemplateSerializer, \
    PaymentAppSerializer


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
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(
            updated_from=user, created_on=user
        )

    def perform_update(self, serializer):
        serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)


class VoIPViewSet(viewsets.ModelViewSet):
    queryset = VoIP.objects.all()  # noqa
    serializer_class = VoIPSerializer
    pagination_class = None
    filterset_class = VoIPFilter

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(
            updated_from=user, created_on=user
        )

    def perform_update(self, serializer):
        serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)


class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()  # noqa
    serializer_class = TemplateSerializer
    pagination_class = None
    filterset_class = TemplateFilter

    def perform_create(self, serializer):
        serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)

    def perform_update(self, serializer):
        serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)


class PaymentAppViewSet(viewsets.ModelViewSet):
    queryset = PaymentApp.objects.all()  # noqa
    serializer_class = PaymentAppSerializer
    pagination_class = None
    filterset_class = PaymentAppFilter

    def perform_create(self, serializer):
        serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)

    def perform_update(self, serializer):
        serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)
