from rest_framework import generics, viewsets  # noqa
from django.contrib.auth import get_user_model

from shipmate.contrib.generics import UpdatePUTAPIView
from shipmate.insights.models import GoalGroup, LeadsInsight
from shipmate.insights.serializers import GoalGroupSerializer, ListLeadsInsightUserSerializer
from shipmate.insights.filters import GoalFilter, LeadsInsightFilter
from shipmate.insights.models import Goal
from shipmate.insights.serializers import (
    ListGoalSerializer, RetrieveGoalSerializer, UpdateGoalSerializer, CreateGoalSerializer,
)
from shipmate.lead_managements.models import Provider


User = get_user_model()


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

from rest_framework.response import Response
from django.db.models import Count


class LeadsInsightUsersAPIView(generics.GenericAPIView):
    queryset = LeadsInsight.objects.all()

    def get(self, request, *args, **kwargs):
        # Get all users
        users = User.objects.all()
        user_labels = [f"{user.first_name} {user.last_name}" for user in users]

        # Get all providers
        providers = Provider.objects.all()

        datasets = []

        for provider in providers:
            # Count LeadsInsight for each user associated with the current provider
            leads_counts = [
                LeadsInsight.objects.filter(user=user, source=provider).count()
                for user in users
            ]
            # Add the data for the current provider to the dataset
            datasets.append({
                'label': provider.name,
                'data': leads_counts,
            })

        # Return data in the required format
        return Response({
            'labels': user_labels,
            'datasets': datasets,
        })
