from drf_spectacular.utils import extend_schema
from rest_framework import generics  # noqa

from shipmate.contrib.generics import UpdatePUTAPIView
from shipmate.users.models import Feature
from shipmate.users.serializers import (
    FeatureSerializer
)

TAG = "users/feature/"


@extend_schema(tags=[TAG])
class FeatureCreateAPIView(generics.CreateAPIView):  # noqa
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


@extend_schema(tags=[TAG])
class FeatureDetailAPIView(generics.RetrieveAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


@extend_schema(tags=[TAG])
class FeatureListAPIView(generics.ListAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    pagination_class = None


@extend_schema(tags=[TAG])  # noqa
class FeatureUpdateAPIView(UpdatePUTAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

    def perform_update(self, serializer):
        serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)


@extend_schema(tags=[TAG])
class FeatureDestroyAPIView(generics.DestroyAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
