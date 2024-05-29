import django_filters

from .models import Carrier


class CarrierFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Carrier.CarrierStatus.choices)

    class Meta:
        model = Carrier
        fields = ['status']
