import django_filters
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import Order
from ..lead_managements.models import Provider

User = get_user_model()


class OrderFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name='status')
    source = django_filters.ModelMultipleChoiceFilter(field_name='source',
                                                      queryset=Provider.objects.all())
    user = django_filters.ModelChoiceFilter(field_name='user', queryset=User.objects.all())
    extraUser = django_filters.ModelChoiceFilter(field_name='extra_user', queryset=User.objects.all())
    q = django_filters.CharFilter(method='custom_filter')

    class Meta:
        model = Order
        fields = ['status', 'source', 'user', 'extraUser', 'q']

    def custom_filter(self, queryset, name, value):
        if value:
            queryset = queryset.filter(
                Q(origin__name__icontains=value) |
                Q(origin__state__name__icontains=value) |
                Q(destination__name__icontains=value) |
                Q(destination__state__name__icontains=value) |
                Q(customer__name__icontains=value) |
                Q(customer__email__icontains=value) |
                Q(customer__phone__icontains=value)
            )

        return queryset
