import django_filters

from .models import Ground, GroundStatus


class GroundFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=GroundStatus.choices)

    class Meta:
        model = Ground
        fields = ['status', ]
