import django_filters
from .models import Customer
from django.db.models import Q


class CustomerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    phone = django_filters.CharFilter(field_name='phone', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    q = django_filters.CharFilter(method='custom_filter')

    def custom_filter(self, queryset, name, value):
        if value:
            queryset = queryset.filter(
                Q(name__icontains=value) |
                Q(last_name__icontains=value) |
                Q(email__icontains=value) |
                Q(phone__icontains=value)
            )

        return queryset

    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'last_name', 'q']
