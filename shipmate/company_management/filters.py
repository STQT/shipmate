import django_filters
from .models import VoIPStatusChoices, VoIP, Merchant, MerchantStatusChoices, TemplateTypeChoices, Template, \
    MerchantTypeChoices, VoIPTypeChoices, PaymentAppTypeChoices, TemplateStatusChoices, PaymentAppStatusChoices, \
    PaymentApp, LeadParsingItem


class VoIPFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=VoIPStatusChoices.choices)
    voip_type = django_filters.ChoiceFilter(choices=VoIPTypeChoices.choices)

    class Meta:
        model = VoIP
        fields = ['status', 'voip_type']


class MerchantFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=MerchantStatusChoices.choices)
    merchant_type = django_filters.ChoiceFilter(choices=MerchantTypeChoices.choices)

    class Meta:
        model = Merchant
        fields = ['status', 'merchant_type']


class TemplateFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=TemplateStatusChoices.choices)
    template_type = django_filters.ChoiceFilter(choices=TemplateTypeChoices.choices)

    class Meta:
        model = Template
        fields = ['status', 'template_type']


class LeadParsingItemFilter(django_filters.FilterSet):
    group = django_filters.NumberFilter(field_name='group', lookup_expr='exact')

    class Meta:
        model = LeadParsingItem
        fields = ['group']


class PaymentAppFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=PaymentAppStatusChoices.choices)
    payment_type = django_filters.ChoiceFilter(choices=PaymentAppTypeChoices.choices)

    class Meta:
        model = PaymentApp
        fields = ['status', 'payment_type']
