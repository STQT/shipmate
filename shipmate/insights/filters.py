import django_filters

from shipmate.insights.models import Goal, GoalGroup


class GoalFilter(django_filters.FilterSet):
    group = django_filters.ModelChoiceFilter(field_name='group', queryset=GoalGroup.objects.all())

    class Meta:
        model = Goal
        fields = ['group']
