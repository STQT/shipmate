import django_filters

from .models import Leads


class LeadsFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name='status')

    class Meta:
        model = Leads
        fields = ['status']
