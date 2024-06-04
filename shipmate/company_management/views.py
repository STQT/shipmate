from rest_framework import generics
from .models import CompanyInfo
from .serializers import CompanyInfoSerializer


class CompanyInfoDetail(generics.RetrieveUpdateAPIView):
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer
