import django_filters
from .models import VoIPStatusChoices, VoIP, Merchant, MerchantStatusChoices, TemplateTypeChoices, Template, \
    MerchantTypeChoices


class VoIPFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=VoIPStatusChoices.choices)

    class Meta:
        model = VoIP
        fields = ['status']


class MerchantFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=MerchantStatusChoices.choices)
    merchant_type = django_filters.ChoiceFilter(choices=MerchantTypeChoices.choices)

    class Meta:
        model = Merchant
        fields = ['status', 'merchant_type']


class TemplateFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=MerchantStatusChoices.choices)
    template_type = django_filters.ChoiceFilter(choices=TemplateTypeChoices.choices)

    class Meta:
        model = Template
        fields = ['status', 'template_type']