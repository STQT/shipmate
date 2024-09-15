import django_filters
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import Quote, QuoteAttachment
from ..contrib.models import QuoteStatusChoices
from ..lead_managements.models import Provider
from django.utils.timezone import now, timedelta

User = get_user_model()


class QuoteFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=QuoteStatusChoices.choices)
    source = django_filters.ModelMultipleChoiceFilter(field_name='source',
                                                      queryset=Provider.objects.all())
    user = django_filters.ModelMultipleChoiceFilter(field_name='user', queryset=User.objects.all())
    extraUser = django_filters.ModelChoiceFilter(field_name='extra_user', queryset=User.objects.all())
    q = django_filters.CharFilter(method='custom_filter')
    availableDate = django_filters.CharFilter(method='available_date_filter')  # New filter
    day = django_filters.CharFilter(method='day_filter')  # New day filter

    class Meta:
        model = Quote
        fields = ['status', 'source', 'user', 'extraUser', 'q', 'trailer_type', 'condition', 'origin', 'destination', 'availableDate', 'day']

    # Custom filter method for 'q'
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

    # New filter method for 'availableDate'
    def available_date_filter(self, queryset, name, value):
        if value.lower() == "first_avail_date":
            # Filtering based on the 'date_est_ship' (first available date)
            return queryset.order_by('date_est_ship')
        elif value.lower() == "last_edited":
            # Filtering based on the 'updated_at' (last edited date)
            return queryset.order_by('-updated_at')
        return queryset

    # New filter method for 'day'
    def day_filter(self, queryset, name, value):
        today = now().date()
        if 'today' in value:
            queryset = queryset.filter(Q(date_est_ship=today) | Q(updated_at__date=today))
        if 'tomorrow' in value:
            tomorrow = today + timedelta(days=1)
            queryset = queryset.filter(Q(date_est_ship=tomorrow) | Q(updated_at__date=tomorrow))
        if 'this_week' in value:
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            queryset = queryset.filter(Q(date_est_ship__range=(start_of_week, end_of_week)) |
                                       Q(updated_at__date__range=(start_of_week, end_of_week)))
        if 'last_week' in value:
            start_of_last_week = today - timedelta(days=today.weekday() + 7)
            end_of_last_week = start_of_last_week + timedelta(days=6)
            queryset = queryset.filter(Q(date_est_ship__range=(start_of_last_week, end_of_last_week)) |
                                       Q(updated_at__date__range=(start_of_last_week, end_of_last_week)))
        return queryset

class QuoteAttachmentFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(field_name='type')

    class Meta:
        model = QuoteAttachment
        fields = ['type']
