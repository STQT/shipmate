from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView  # noqa

from shipmate.lead_managements.serializers import *
from shipmate.contrib.generics import UpdatePUTAPIView

DISTRIBUTION_TAG = "distribution"


@extend_schema(tags=[DISTRIBUTION_TAG])
class ListDistributionAPIView(ListAPIView):  # noqa
    queryset = Distribution.objects.all()
    pagination_class = None
    serializer_class = DistributionSmallDataSerializer


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
