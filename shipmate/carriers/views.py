from drf_spectacular.utils import extend_schema
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
    DestroyAPIView, CreateAPIView
)

from shipmate.carriers.filters import CarrierFilter
from shipmate.carriers.models import Carrier
from shipmate.carriers.serializers import (
    ListCarrierSerializer, CreateCarrierSerializer, UpdateCarrierSerializer,
    RetrieveCarrierSerializer
)
from shipmate.contrib.generics import UpdatePUTAPIView


class ListCarrierAPIView(ListAPIView):  # noqa
    queryset = Carrier.objects.all()
    serializer_class = ListCarrierSerializer
    filterset_class = CarrierFilter
    pagination_class = None
    ordering = ("-id",)


class CreateCarrierAPIView(CreateAPIView):  # noqa
    queryset = Carrier.objects.all()
    serializer_class = CreateCarrierSerializer


@extend_schema(
    deprecated=True,
    description="This endpoint is deprecated and will be removed in future versions."
)
class UpdateCarrierAPIView(UpdatePUTAPIView):
    queryset = Carrier.objects.all()
    serializer_class = UpdateCarrierSerializer


class DeleteCarrierAPIView(DestroyAPIView):
    queryset = Carrier.objects.all()
    serializer_class = CreateCarrierSerializer


@extend_schema(
    deprecated=True,
    description="This endpoint is deprecated and will be removed in future versions.",
)
class DetailCarrierAPIView(RetrieveAPIView):
    queryset = Carrier.objects.all()
    serializer_class = RetrieveCarrierSerializer
