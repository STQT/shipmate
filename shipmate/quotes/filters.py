import django_filters
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import Quote, QuoteAttachment
from ..contrib.models import QuoteStatusChoices, TrailerTypeChoices, ConditionChoices
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
    period_date_from = django_filters.DateFilter(field_name='date_est_ship', lookup_expr='gte', method='period_filter_from')
    period_date_to = django_filters.DateFilter(field_name='date_est_ship', lookup_expr='lte', method='period_filter_to')

    # Trailer type and condition filters (as ChoiceFilters)
    trailer_type = django_filters.ChoiceFilter(choices=TrailerTypeChoices.choices)
    condition = django_filters.ChoiceFilter(choices=ConditionChoices.choices)

    # Origin and Destination state filters
    origin_state = django_filters.CharFilter(method='origin_state_filter')
    destination_state = django_filters.CharFilter(method='destination_state_filter')

    class Meta:
        model = Quote
        fields = ['status', 'source', 'user', 'extraUser', 'q', 'trailer_type', 'condition', 'origin_state', 'destination_state', 'availableDate', 'day', 'period_date_from', 'period_date_to']

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
        if value.lower() == "first avail date":
            # Filtering based on the 'date_est_ship' (first available date)
            return queryset.order_by('date_est_ship')
        elif value.lower() == "last edited":
            # Filtering based on the 'updated_at' (last edited date)
            return queryset.order_by('-updated_at')
        return queryset

    # Updated filter method for 'day' based on 'created_at' field
    def day_filter(self, queryset, name, value):
        today = now().date()
        if 'today' in value:
            queryset = queryset.filter(created_at__date=today)
        if 'tomorrow' in value:
            tomorrow = today + timedelta(days=1)
            queryset = queryset.filter(created_at__date=tomorrow)
        if 'this_week' in value:
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            queryset = queryset.filter(created_at__date__range=(start_of_week, end_of_week))
        if 'last_week' in value:
            start_of_last_week = today - timedelta(days=today.weekday() + 7)
            end_of_last_week = start_of_last_week + timedelta(days=6)
            queryset = queryset.filter(created_at__date__range=(start_of_last_week, end_of_last_week))
        return queryset

    # New filter method for 'period_date_from'
    def period_filter_from(self, queryset, name, value):
        # Filters quotes from the given start date on either 'date_est_ship' or 'updated_at'
        queryset = queryset.filter(Q(date_est_ship__gte=value) | Q(updated_at__date__gte=value))
        return queryset

    # New filter method for 'period_date_to'
    def period_filter_to(self, queryset, name, value):
        # Filters quotes up to the given end date on either 'date_est_ship' or 'updated_at'
        queryset = queryset.filter(Q(date_est_ship__lte=value) | Q(updated_at__date__lte=value))
        return queryset

    # New filter method for 'origin_state' based on the State name of the origin city
    def origin_state_filter(self, queryset, name, value):
        return queryset.filter(origin__state__name__icontains=value)

    # New filter method for 'destination_state' based on the State name of the destination city
    def destination_state_filter(self, queryset, name, value):
        return queryset.filter(destination__state__name__icontains=value)

class QuoteAttachmentFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(field_name='type')

    class Meta:
        model = QuoteAttachment
        fields = ['type']
