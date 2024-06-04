from drf_spectacular.utils import extend_schema

from rest_framework import viewsets

from .filters import InternationalFilter, HawaiiFilter, GroundFilter
from .models import Ground, Hawaii, International
from rest_framework.permissions import IsAuthenticated
from shipmate.contract.serializers import GroundSerializer, HawaiiSerializer, InternationalSerializer


@extend_schema(tags=["contracts/ground"])
class GroundViewSet(viewsets.ModelViewSet):
    queryset = Ground.objects.all()
    serializer_class = GroundSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = GroundFilter

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_from=self.request.user)


@extend_schema(tags=["contracts/hawaii"])
class HawaiiViewSet(viewsets.ModelViewSet):
    queryset = Hawaii.objects.all()
    serializer_class = HawaiiSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = HawaiiFilter

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_from=self.request.user)


@extend_schema(tags=["contracts/international"])
class InternationalViewSet(viewsets.ModelViewSet):
    queryset = International.objects.all()
    serializer_class = InternationalSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = InternationalFilter

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_from=self.request.user)
