from django.contrib import admin

from shipmate.company_management.models import CompanyInfo, Merchant, VoIP


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'mainline', 'fax', 'email', 'address']


@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'merchant_type']


@admin.register(VoIP)
class VoIPAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'voip_type']
