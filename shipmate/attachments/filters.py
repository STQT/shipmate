import django_filters
from django.contrib.auth import get_user_model
from django.db.models import Q

from datetime import datetime, timedelta

from .models import TaskAttachment

User = get_user_model()


class TaskAttachmentFilter(django_filters.FilterSet):
    type = django_filters.ChoiceFilter(choices=TaskAttachment.TypeChoices.choices)
    status = django_filters.ChoiceFilter(choices=TaskAttachment.StatusChoice.choices)

    user = django_filters.ModelMultipleChoiceFilter(field_name='user', queryset=User.objects.all())
    q = django_filters.CharFilter(method='custom_filter')

    due = django_filters.BooleanFilter(method='filter_due')
    to_do = django_filters.BooleanFilter(method='filter_to_do')
    today = django_filters.BooleanFilter(method='filter_today')
    tomorrow = django_filters.BooleanFilter(method='filter_tomorrow')
    this_week = django_filters.BooleanFilter(method='filter_this_week')
    next_week = django_filters.BooleanFilter(method='filter_next_week')

    class Meta:
        model = TaskAttachment
        fields = [
            'type', 'status', 'user', 'q',
            'due', 'to_do', 'today', 'tomorrow', 'this_week', 'next_week'
        ]

    def custom_filter(self, queryset, name, value):
        if value:
            queryset = queryset.filter(
                Q(text__icontains=value)
            )

        return queryset

    def filter_status(self, queryset, name, value):
        # Check if 'all' is passed for status, return all records if true
        if value == 'all':
            return queryset
        return queryset.filter(status=value)

    def filter_due(self, queryset, name, value):
        if value:
            now = datetime.now()
            queryset = queryset.filter(end_time__lt=now)
        return queryset

    def filter_to_do(self, queryset, name, value):
        if value:
            now = datetime.now()
            queryset = queryset.filter(end_time__gte=now)
        return queryset

    def filter_today(self, queryset, name, value):
        if value:
            today = datetime.now()
            queryset = queryset.filter(start_time__date=today.date())
        return queryset

    def filter_tomorrow(self, queryset, name, value):
        if value:
            tomorrow = datetime.now() + timedelta(days=1)
            queryset = queryset.filter(start_time__date=tomorrow.date())
        return queryset

    def filter_this_week(self, queryset, name, value):
        if value:
            today = datetime.now()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            queryset = queryset.filter(start_time__date__gte=start_of_week.date(),
                                       start_time__date__lte=end_of_week.date())
        return queryset

    def filter_next_week(self, queryset, name, value):
        if value:
            today = datetime.now()
            start_of_next_week = today + timedelta(days=(7 - today.weekday()))
            end_of_next_week = start_of_next_week + timedelta(days=6)
            queryset = queryset.filter(start_time__date__gte=start_of_next_week.date(),
                                       start_time__date__lte=end_of_next_week.date())
        return queryset
