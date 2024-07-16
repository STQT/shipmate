from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView  # noqa

from shipmate.lead_managements.filters import DistributionFilter
from shipmate.contrib.generics import UpdatePUTAPIView
from shipmate.lead_managements.models import Distribution
from shipmate.lead_managements.serializers import (
    ListDistributionSerializer, UpdateDistributionSerializer,
    DetailDistributionSerializer
)

DISTRIBUTION_TAG = "distribution"


@extend_schema(tags=[DISTRIBUTION_TAG])
class ListDistributionAPIView(ListAPIView):  # noqa
    queryset = Distribution.objects.filter(user__is_active=True)
    pagination_class = None
    serializer_class = ListDistributionSerializer
    filterset_class = DistributionFilter


@extend_schema(tags=[DISTRIBUTION_TAG])
class UpdateDistributionAPIView(UpdatePUTAPIView):
    queryset = Distribution.objects.all()
    serializer_class = UpdateDistributionSerializer

    def perform_update(self, serializer):
        serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)


@extend_schema(tags=[DISTRIBUTION_TAG])
class DetailDistributionAPIView(RetrieveAPIView):
    queryset = Distribution.objects.prefetch_related("logs")
    serializer_class = DetailDistributionSerializer
