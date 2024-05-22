from rest_framework import generics # noqa

from shipmate.contrib.generics import UpdatePUTAPIView
from shipmate.users.models import Team
from shipmate.users.serializers import (
    TeamSerializer
)


class TeamCreateAPIView(generics.CreateAPIView):  # noqa
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamDetailAPIView(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamListAPIView(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamUpdateAPIView(UpdatePUTAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamDestroyAPIView(generics.DestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

