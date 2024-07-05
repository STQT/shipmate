import django_filters
from .models import CarMarks, CarsModel


class CarMarksFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='custom_filter')

    class Meta:
        model = CarMarks
        fields = ['q']

    def custom_filter(self, queryset, name, value):
        if value:
            return queryset.filter(name__icontains=value)
        return queryset


class CarsModelFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='custom_filter')
    mark = django_filters.CharFilter(field_name='mark__id')

    class Meta:
        model = CarsModel
        fields = ['q', 'mark']

    def custom_filter(self, queryset, name, value):
        if value:
            return queryset.filter(name__icontains=value)
        return queryset
