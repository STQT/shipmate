import django_filters

from shipmate.lead_managements.models import Provider, Distribution


class ProviderFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Provider.ProviderStatusChoices.choices)
    type = django_filters.ChoiceFilter(choices=Provider.ProviderTypeChoices.choices)

    class Meta:
        model = Provider
        fields = ['status', 'type']


class DistributionFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Distribution.DistributionStatusChoices.choices)

    class Meta:
        model = Distribution
        fields = ['status']
