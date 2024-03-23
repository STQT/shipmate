import django_filters
from .models import Customer


class CustomerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    phone = django_filters.CharFilter(field_name='phone', lookup_expr='icontains')

    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone']
