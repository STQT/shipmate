from rest_framework import generics, viewsets  # noqa

from shipmate.contrib.generics import UpdatePUTAPIView
from shipmate.insights.models import GoalGroup, LeadsInsight
from shipmate.insights.serializers import GoalGroupSerializer, ListLeadsInsightUserSerializer
from shipmate.insights.filters import GoalFilter, LeadsInsightFilter
from shipmate.insights.models import Goal
from shipmate.insights.serializers import (
    ListGoalSerializer, RetrieveGoalSerializer, UpdateGoalSerializer, CreateGoalSerializer,
)


class GoalCreateAPIView(generics.CreateAPIView):  # noqa
    queryset = Goal.objects.all()
    serializer_class = CreateGoalSerializer


class GoalDetailAPIView(generics.RetrieveAPIView):
    queryset = Goal.objects.all()
    serializer_class = RetrieveGoalSerializer


class GoalListAPIView(generics.ListAPIView):
    queryset = Goal.objects.all()
    serializer_class = ListGoalSerializer
    filterset_class = GoalFilter
    pagination_class = None


class GoalUpdateAPIView(UpdatePUTAPIView):
    queryset = Goal.objects.all()
    serializer_class = UpdateGoalSerializer


class GoalDestroyAPIView(generics.DestroyAPIView):
    queryset = Goal.objects.all()
    serializer_class = UpdateGoalSerializer


class GoalGroupViewSet(viewsets.ModelViewSet):
    queryset = GoalGroup.objects.all()
    serializer_class = GoalGroupSerializer


# Lead Insight

class LeadsInsightUsersAPIView(generics.ListAPIView):
    queryset = LeadsInsight.objects.all()
    serializer_class = ListLeadsInsightUserSerializer
    filterset_class = LeadsInsightFilter
    pagination_class = None
