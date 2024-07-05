from drf_spectacular.utils import extend_schema
from rest_framework import generics  # noqa

from shipmate.contrib.generics import UpdatePUTAPIView
from shipmate.users.filters import TeamFilter
from shipmate.users.models import Team
from shipmate.users.serializers import (
    TeamSerializer, TeamDetailSerializer
)


TAG = "users/team/"


@extend_schema(tags=[TAG])
class TeamCreateAPIView(generics.CreateAPIView):  # noqa
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


@extend_schema(tags=[TAG])
class TeamDetailAPIView(generics.RetrieveAPIView):
    queryset = Team.objects.prefetch_related("logs")
    serializer_class = TeamDetailSerializer


@extend_schema(tags=[TAG])
class TeamListAPIView(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filterset_class = TeamFilter
    pagination_class = None


@extend_schema(tags=[TAG])
class TeamUpdateAPIView(UpdatePUTAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def perform_update(self, serializer):
        serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)


@extend_schema(tags=[TAG])
class TeamDestroyAPIView(generics.DestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
