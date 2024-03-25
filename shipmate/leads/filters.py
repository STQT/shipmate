import django_filters

from .models import Leads, LeadsAttachment


class LeadsFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name='status')

    class Meta:
        model = Leads
        fields = ['status']


class LeadsAttachmentFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(field_name='type')

    class Meta:
        model = LeadsAttachment
        fields = ['type']
