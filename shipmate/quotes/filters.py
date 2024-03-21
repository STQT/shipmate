import django_filters

from .models import Quote


class QuoteFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name='status')

    class Meta:
        model = Quote
        fields = ['status']
