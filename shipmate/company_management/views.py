from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import VoIPFilter, MerchantFilter, TemplateFilter, PaymentAppFilter, LeadParsingItemFilter
from .models import CompanyInfo, Merchant, VoIP, Template, PaymentApp, LeadParsingGroup, LeadParsingValue, \
    LeadParsingItem
from .serializers import (
    CompanyInfoSerializer, MerchantSerializer, VoIPSerializer, TemplateSerializer,
    PaymentAppSerializer, LeadParsingGroupSerializer, LeadParsingValueSerializer,
    LeadParsingSmallSerializer, CreateLeadParsingValueSerializer
)
from ..contrib.generics import UpdatePUTAPIView


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


class LeadParsingGroupAllListView(APIView):
    serializer_class = LeadParsingGroupSerializer(many=True)

    def get(self, request, *args, **kwargs):
        groups = LeadParsingGroup.objects.all()
        serializer = LeadParsingGroupSerializer(groups, many=True)
        return Response(serializer.data)


class LeadParsingGroupListView(generics.ListAPIView):
    serializer_class = LeadParsingGroupSerializer
    pagination_class = None
    queryset = LeadParsingGroup.objects.all()


class LeadParsingItemListView(generics.ListAPIView):
    serializer_class = LeadParsingSmallSerializer
    queryset = LeadParsingItem.objects.all()
    pagination_class = None
    filterset_class = LeadParsingItemFilter


class LeadParsingValuePUTView(UpdatePUTAPIView):
    serializer_class = LeadParsingValueSerializer
    queryset = LeadParsingValue.objects.all()


class LeadParsingValueDeleteView(generics.DestroyAPIView):
    serializer_class = LeadParsingValueSerializer
    queryset = LeadParsingValue.objects.all()


class CreateLeadParsingValueView(generics.CreateAPIView):
    serializer_class = CreateLeadParsingValueSerializer
    queryset = LeadParsingValue.objects.all()
