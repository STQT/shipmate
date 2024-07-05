from django.contrib import admin

from shipmate.company_management.models import (
    CompanyInfo, Merchant, VoIP, Template, CompanyInfoLog, MerchantLog,
    VoIPLog, TemplateLog, PaymentAppLog, PaymentApp, LeadParsingGroup,
    LeadParsingValue, LeadParsingItem
)


class CompanyInfoLogInline(admin.TabularInline):
    model = CompanyInfoLog
    extra = 0


class MerchantLogInline(admin.TabularInline):
    model = MerchantLog
    extra = 0


class VoIPLogInline(admin.TabularInline):
    model = VoIPLog
    extra = 0


class TemplateLogInline(admin.TabularInline):
    model = TemplateLog
    extra = 0


class PaymentAppLogInline(admin.TabularInline):
    model = PaymentAppLog
    extra = 0


class LeadParsingValueInline(admin.TabularInline):
    model = LeadParsingValue
    extra = 0


class LeadParsingItemInline(admin.TabularInline):
    model = LeadParsingItem
    extra = 0


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'mainline', 'fax', 'email', 'address']
    inlines = [CompanyInfoLogInline]


@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'merchant_type']
    inlines = [MerchantLogInline]


@admin.register(VoIP)
class VoIPAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'voip_type']
    inlines = [VoIPLogInline]


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'template_type']
    inlines = [TemplateLogInline]


@admin.register(PaymentApp)
class PaymentAppAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'payment_type']
    inlines = [PaymentAppLogInline]


@admin.register(LeadParsingGroup)
class LeadParsingGroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [LeadParsingItemInline]


@admin.register(LeadParsingItem)
class LeadParsingItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    inlines = [LeadParsingValueInline]
