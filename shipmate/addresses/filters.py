import django_filters
from .models import City, States


class CityFilter(django_filters.FilterSet):
    state = django_filters.CharFilter(field_name='state__id')
    q = django_filters.CharFilter(method='custom_filter')

    class Meta:
        model = City
        fields = ['state', 'q']

    def custom_filter(self, queryset, name, value):
        if value:
            return queryset.filter(name__icontains=value) | queryset.filter(zip__icontains=value)
        return queryset


class StatesFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='custom_filter')

    class Meta:
        model = States
        fields = ['q']

    def custom_filter(self, queryset, name, value):
        if value:
            return queryset.filter(code__icontains=value)
        return queryset
