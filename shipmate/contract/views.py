from drf_spectacular.utils import extend_schema

from rest_framework import viewsets
from .models import Ground, Hawaii, International
from shipmate.contract.serializers import GroundSerializer, HawaiiSerializer, InternationalSerializer


@extend_schema(tags=["contracts/ground"])
class GroundViewSet(viewsets.ModelViewSet):
    queryset = Ground.objects.all()
    serializer_class = GroundSerializer


@extend_schema(tags=["contracts/hawaii"])
class HawaiiViewSet(viewsets.ModelViewSet):
    queryset = Hawaii.objects.all()
    serializer_class = HawaiiSerializer


@extend_schema(tags=["contracts/international"])
class InternationalViewSet(viewsets.ModelViewSet):
    queryset = International.objects.all()
    serializer_class = InternationalSerializer
