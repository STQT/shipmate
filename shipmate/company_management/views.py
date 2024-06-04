from rest_framework import generics, viewsets
from .models import CompanyInfo, Merchant, VoIP
from .serializers import CompanyInfoSerializer, MerchantSerializer, VoIPSerializer


class CompanyInfoDetail(generics.RetrieveUpdateAPIView):
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer


class MerchantViewSet(viewsets.ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer


class VoIPViewSet(viewsets.ModelViewSet):
    queryset = VoIP.objects.all()
    serializer_class = VoIPSerializer
