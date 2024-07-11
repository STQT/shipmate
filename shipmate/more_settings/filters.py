import django_filters

from shipmate.more_settings.models import Automation


class AutomationFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Automation.StatusChoices.choices)
    steps = django_filters.ChoiceFilter(choices=Automation.StepsChoices.choices)

    class Meta:
        model = Automation
        fields = ['status', 'steps']
