import django_filters

from .models import Carrier


class CarrierFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Carrier.CarrierStatus.choices)
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Carrier
        fields = ['status', 'name']
