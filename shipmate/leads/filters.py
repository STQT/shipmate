import django_filters

from .models import Leads, LeadsAttachment
from ..lead_managements.models import Provider


class LeadsFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name='status')
    source = django_filters.ModelMultipleChoiceFilter(field_name='source',
                                                      queryset=Provider.objects.all())

    class Meta:
        model = Leads
        fields = ['status']


class LeadsAttachmentFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(field_name='type')

    class Meta:
        model = LeadsAttachment
        fields = ['type']
