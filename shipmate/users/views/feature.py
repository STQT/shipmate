from rest_framework import generics # noqa

from shipmate.contrib.generics import UpdatePUTAPIView
from shipmate.users.models import Feature
from shipmate.users.serializers import (
    FeatureSerializer
)


class FeatureCreateAPIView(generics.CreateAPIView):  # noqa
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


class FeatureDetailAPIView(generics.RetrieveAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


class FeatureListAPIView(generics.ListAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


class FeatureUpdateAPIView(UpdatePUTAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


class FeatureDestroyAPIView(generics.DestroyAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

