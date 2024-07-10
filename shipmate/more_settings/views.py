from rest_framework import generics  # noqa

from shipmate.contrib.generics import UpdatePUTAPIView
from shipmate.more_settings.filters import AutomationFilter
from shipmate.more_settings.models import Automation
from shipmate.more_settings.serializers import (
    AutomationSerializer, RetrieveAutomationSerializer, UpdateAutomationSerializer, CreateAutomationSerializer,
)


class AutomationCreateAPIView(generics.CreateAPIView):  # noqa
    queryset = Automation.objects.all()
    serializer_class = CreateAutomationSerializer


class AutomationDetailAPIView(generics.RetrieveAPIView):
    queryset = Automation.objects.prefetch_related("logs")
    serializer_class = RetrieveAutomationSerializer


class AutomationListAPIView(generics.ListAPIView):
    queryset = Automation.objects.all()
    serializer_class = AutomationSerializer
    filterset_class = AutomationFilter
    pagination_class = None


class AutomationUpdateAPIView(UpdatePUTAPIView):
    queryset = Automation.objects.all()
    serializer_class = UpdateAutomationSerializer

    def perform_update(self, serializer):
        serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)


class AutomationDestroyAPIView(generics.DestroyAPIView):
    queryset = Automation.objects.all()
    serializer_class = AutomationSerializer
