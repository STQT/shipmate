from rest_framework import generics, viewsets  # noqa
from django.contrib.auth import get_user_model

from shipmate.contrib.generics import UpdatePUTAPIView
from shipmate.insights.models import GoalGroup, LeadsInsight
from shipmate.insights.serializers import GoalGroupSerializer, ListLeadsInsightUserSerializer, \
    ListLeadsInsightSerializer
from shipmate.insights.filters import GoalFilter, LeadsInsightFilter
from shipmate.insights.models import Goal
from shipmate.insights.serializers import (
    ListGoalSerializer, RetrieveGoalSerializer, UpdateGoalSerializer, CreateGoalSerializer,
)

from rest_framework.response import Response
from django.utils.timezone import now
from django.db.models import Count
from django.db.models.functions import TruncDay
from datetime import timedelta
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



class LeadsInsightDaysAPIView(generics.GenericAPIView):
    queryset = LeadsInsight.objects.all()

    def get(self, request, *args, **kwargs):
        # Get the date range for the last 6 days
        today = now().date()
        start_date = today - timedelta(days=5)  # 6 days including today

        # Get all providers
        providers = Provider.objects.all()

        # Create labels for the last 6 days
        labels = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6)]

        datasets = []

        for provider in providers:
            # Count LeadsInsight for each day for the current provider
            leads_counts = (
                LeadsInsight.objects
                .filter(created_at__date__gte=start_date, source=provider)
                .annotate(day=TruncDay('created_at'))
                .values('day')
                .annotate(count=Count('id'))
                .order_by('day')
            )

            # Create a dictionary for each day initialized with zero
            leads_data_by_day = {day: 0 for day in labels}

            # Fill in the actual counts from the query result
            for entry in leads_counts:
                day_str = entry['day'].strftime('%Y-%m-%d')
                leads_data_by_day[day_str] = entry['count']

            # Add the data for the current provider to the dataset
            datasets.append({
                'label': provider.name,
                'data': [leads_data_by_day[day] for day in labels],
            })

        # Return data in the required format
        return Response({
            'labels': labels,
            'datasets': datasets,
        })


class LeadsInsightAPIView(generics.ListAPIView):
    queryset = LeadsInsight.objects.all()
    serializer_class = ListLeadsInsightSerializer
    pagination_class = None


