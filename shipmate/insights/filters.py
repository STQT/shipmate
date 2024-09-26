import django_filters

from shipmate.insights.models import Goal, GoalGroup, LeadsInsight
from shipmate.lead_managements.models import Provider


class GoalFilter(django_filters.FilterSet):
    group = django_filters.ModelChoiceFilter(field_name='group', queryset=GoalGroup.objects.all())

    class Meta:
        model = Goal
        fields = ['group']


class LeadsInsightFilter(django_filters.FilterSet):
    source = django_filters.ModelChoiceFilter(field_name='source', queryset=Provider.objects.all())

    class Meta:
        model = LeadsInsight
        fields = ['source']
