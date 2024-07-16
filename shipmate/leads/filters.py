import django_filters
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import Leads, LeadsAttachment
from ..lead_managements.models import Provider

User = get_user_model()


class LeadsFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name='status')
    source = django_filters.ModelMultipleChoiceFilter(field_name='source',
                                                      queryset=Provider.objects.all())
    user = django_filters.ModelMultipleChoiceFilter(field_name='user', queryset=User.objects.all())
    extraUser = django_filters.ModelChoiceFilter(field_name='extra_user', queryset=User.objects.all())
    q = django_filters.CharFilter(method='custom_filter')

    class Meta:
        model = Leads
        fields = ['status', 'source', 'user', 'extraUser', 'q']

    def custom_filter(self, queryset, name, value):
        value = value.replace("(", "").replace(")", "").replace(" ", "").replace("-", "")
        if value:
            q_objects = (Q(origin__name__icontains=value) |
                         Q(origin__state__name__icontains=value) |
                         Q(destination__name__icontains=value) |
                         Q(destination__state__name__icontains=value) |
                         Q(customer__name__icontains=value) |
                         Q(customer__email__icontains=value) |
                         Q(customer__phone__icontains=value))

            if value.isdigit():
                q_objects |= Q(id=value)
            queryset = queryset.filter(q_objects)
        return queryset


class LeadsAttachmentFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(field_name='type')

    class Meta:
        model = LeadsAttachment
        fields = ['type']
