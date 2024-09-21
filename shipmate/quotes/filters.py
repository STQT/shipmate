from datetime import datetime

import django_filters
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.exceptions import ValidationError

from .models import Quote, QuoteAttachment
from ..attachments.models import TaskAttachment
from ..cars.models import CarMarks
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
    period_date_from = django_filters.DateFilter(method='period_date_filter', label='Period From')
    period_date_to = django_filters.DateFilter(method='period_date_filter', label='Period To')

    # Trailer type and condition filters (as ChoiceFilters)
    trailer_type = django_filters.ChoiceFilter(choices=TrailerTypeChoices.choices)
    condition = django_filters.ChoiceFilter(choices=ConditionChoices.choices)

    # Origin and Destination state filters
    origin_state = django_filters.CharFilter(method='origin_state_filter')
    destination_state = django_filters.CharFilter(method='destination_state_filter')

    vehicle_id = django_filters.ModelChoiceFilter(
        field_name="quote_vehicles__vehicle__mark",
        queryset=CarMarks.objects.all(),
        label="Vehicle"
    )

    time_zones = django_filters.CharFilter(method='time_zone_filter')  # New time_zone filter

    class Meta:
        model = Quote
        fields = ['status', 'source', 'user', 'extraUser', 'q', 'trailer_type', 'condition', 'origin_state', 'destination_state', 'availableDate', 'day', 'period_date_from', 'period_date_to', 'vehicle_id']

    TIMEZONE_AREA_CODES = {
        'EST': ['201', '212', '305', '718', '929', '617', '202', '646'],
        'CT': ['312', '469', '713', '214', '281', '773'],
        'MT': ['303', '406', '505', '575', '720'],
        'PST': ['213', '310', '415', '702', '619', '818']
    }



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

    def time_zone_filter(self, queryset, name, value):
        """
        Custom filter method to filter quotes based on the time zone of the phone number.
        :param queryset: The original queryset
        :param name: The name of the filter field (time_zone)
        :param value: The value of the filter (EST, CT, MT, PST)
        :return: Filtered queryset
        """
        # Get area codes for the given time zone
        area_codes = self.TIMEZONE_AREA_CODES.get(value.upper(), [])

        if area_codes:
            # Remove any characters like '(', ')', spaces, or dashes for proper matching
            query_regex = r'^(\({0}\))|^({0})'.format('|'.join(area_codes))

            # Filter quotes based on the customer phone number's area code
            return queryset.filter(customer__phone__regex=query_regex)
        return queryset

    # New filter method for 'availableDate'
    def available_date_filter(self, queryset, name, value):

        pass
        # if value.lower() == "first_avail_date":
        #     # Filtering based on the 'date_est_ship' (first available date)
        #     return queryset.order_by('date_est_ship')
        # elif value.lower() == "last_edited":
        #     # Filtering based on the 'updated_at' (last edited date)
        #     return queryset.order_by('-updated_at')
        # elif value.lower() == "quoted":
        #     # Filtering based on the 'updated_at' (last edited date)
        #     return queryset.order_by('-quoted')
        # return queryset

    # Updated filter method for 'day' based on 'created_at' field
    def day_filter(self, queryset, name, value):
        today = now().date()
        available_date_filter_value = self.data['available_date']

        if available_date_filter_value:
            if available_date_filter_value.lower() == "first_available_date":

                if 'today' in value.lower():
                    queryset = queryset.filter(date_est_ship=today)
                if 'tomorrow' in value.lower():
                    tomorrow = today + timedelta(days=1)
                    queryset = queryset.filter(date_est_ship=tomorrow)
                if 'this_week' in value.lower():
                    start_of_week = today - timedelta(days=today.weekday())
                    end_of_week = start_of_week + timedelta(days=6)
                    queryset = queryset.filter(date_est_ship__range=(start_of_week, end_of_week))
                if 'last_week' in value.lower():
                    start_of_last_week = today - timedelta(days=today.weekday() + 7)
                    end_of_last_week = start_of_last_week + timedelta(days=6)
                    queryset = queryset.filter(date_est_ship__range=(start_of_last_week, end_of_last_week))
            elif available_date_filter_value.lower() == "last_edited":
                # Filtering based on the 'updated_at' (last edited date)
                if 'today' in value.lower():
                    queryset = queryset.filter(updated_at__date=today)
                if 'tomorrow' in value.lower():
                    tomorrow = today + timedelta(days=1)
                    queryset = queryset.filter(updated_at__date=tomorrow)
                if 'this_week' in value.lower():
                    start_of_week = today - timedelta(days=today.weekday())
                    end_of_week = start_of_week + timedelta(days=6)
                    queryset = queryset.filter(updated_at__date__range=(start_of_week, end_of_week))
                if 'last_week' in value.lower():
                    start_of_last_week = today - timedelta(days=today.weekday() + 7)
                    end_of_last_week = start_of_last_week + timedelta(days=6)
                    queryset = queryset.filter(updated_at__date__range=(start_of_last_week, end_of_last_week))
            elif available_date_filter_value.lower() == "quoted":
                # Filtering based on the 'updated_at' (last edited date)
                if 'today' in value.lower():
                    queryset = queryset.filter(quote_dates__quoted__date=today)
                if 'tomorrow' in value.lower():
                    tomorrow = today + timedelta(days=1)
                    queryset = queryset.filter(quote_dates__quoted__date=tomorrow)
                if 'this_week' in value.lower():
                    start_of_week = today - timedelta(days=today.weekday())
                    end_of_week = start_of_week + timedelta(days=6)
                    queryset = queryset.filter(quote_dates__quoted__date__range=(start_of_week, end_of_week))
                if 'last_week' in value.lower():
                    start_of_last_week = today - timedelta(days=today.weekday() + 7)
                    end_of_last_week = start_of_last_week + timedelta(days=6)
                    queryset = queryset.filter(quote_dates__quoted__date__range=(start_of_last_week, end_of_last_week))
            elif available_date_filter_value.lower() == "task":
                # Filtering by task deadline (using `TaskAttachment.date`)
                # Get task deadlines based on the date filters

                if 'today' in value.lower():
                    task_attachments = TaskAttachment.objects.filter(date=today)
                elif 'tomorrow' in value.lower():
                    tomorrow = today + timedelta(days=1)
                    task_attachments = TaskAttachment.objects.filter(date=tomorrow)
                elif 'this_week' in value.lower():
                    start_of_week = today - timedelta(days=today.weekday())
                    end_of_week = start_of_week + timedelta(days=6)
                    task_attachments = TaskAttachment.objects.filter(date__range=(start_of_week, end_of_week))
                elif 'last_week' in value.lower():
                    start_of_last_week = today - timedelta(days=today.weekday() + 7)
                    end_of_last_week = start_of_last_week + timedelta(days=6)
                    task_attachments = TaskAttachment.objects.filter(date__range=(start_of_last_week, end_of_last_week))
                else:
                    task_attachments = TaskAttachment.objects.none()  # No valid filter case

                    # Now filter quotes based on the obtained task attachments
                if task_attachments.exists():
                    # Assuming 'link' in QuoteAttachment corresponds to some ID in Quote
                    queryset = queryset.filter(
                        id__in=QuoteAttachment.objects.filter(
                            link__in=task_attachments.values_list('id', flat=True)).values_list('quote_id', flat=True)
                    )
            return queryset
        return queryset
            # if 'today' in value:
            #     queryset = queryset.filter(created_at__date=today)
            # if 'tomorrow' in value:
            #     tomorrow = today + timedelta(days=1)
            #     queryset = queryset.filter(created_at__date=tomorrow)
            # if 'this_week' in value:
            #     start_of_week = today - timedelta(days=today.weekday())
            #     end_of_week = start_of_week + timedelta(days=6)
            #     queryset = queryset.filter(created_at__date__range=(start_of_week, end_of_week))
            # if 'last_week' in value:
            #     start_of_last_week = today - timedelta(days=today.weekday() + 7)
            #     end_of_last_week = start_of_last_week + timedelta(days=6)
            #     queryset = queryset.filter(created_at__date__range=(start_of_last_week, end_of_last_week))
            # return queryset

    # New filter method for 'period_date_from'
    def period_date_filter(self, queryset, name, value):
        period_date_from = self.data.get('period_date_from', None)
        period_date_to = self.data.get('period_date_to', None)
        available_date_filter_value = self.data.get('available_date', None)

        if period_date_from and period_date_to and available_date_filter_value:
            # Convert strings to date objects
            try:
                period_date_from = datetime.strptime(period_date_from, '%Y-%m-%d').date()
                period_date_to = datetime.strptime(period_date_to, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError("Enter a valid date format, expected YYYY-MM-DD.")

            if available_date_filter_value.lower() == "first_available_date":
                # Filter by 'date_est_ship'
                queryset = queryset.filter(date_est_ship__range=(period_date_from, period_date_to))

            elif available_date_filter_value.lower() == "last_edited":
                # Filter by 'updated_at' field
                queryset = queryset.filter(updated_at__date__range=(period_date_from, period_date_to))

            elif available_date_filter_value.lower() == "quoted":
                # Filter by 'quote_dates__quoted'
                queryset = queryset.filter(quote_dates__quoted__range=(period_date_from, period_date_to))

        return queryset

    # New filter method for 'origin_state' based on the State name of the origin city
    def origin_state_filter(self, queryset, name, value):
        return queryset.filter(origin__state__code__icontains=value)

    # New filter method for 'destination_state' based on the State name of the destination city
    def destination_state_filter(self, queryset, name, value):
        return queryset.filter(destination__state__code__icontains=value)

class QuoteAttachmentFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(field_name='type')

    class Meta:
        model = QuoteAttachment
        fields = ['type']
