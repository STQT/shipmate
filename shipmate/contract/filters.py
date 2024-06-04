import django_filters

from .models import Ground, GroundStatus, Hawaii, International


class GroundFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=GroundStatus.choices)

    class Meta:
        model = Ground
        fields = ['status', ]


class HawaiiFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=GroundStatus.choices)

    class Meta:
        model = Hawaii
        fields = ['status', ]


class InternationalFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=GroundStatus.choices)

    class Meta:
        model = International
        fields = ['status', ]
