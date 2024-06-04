from django.contrib import admin

from shipmate.company_management.models import CompanyInfo


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'mainline', 'fax', 'email', 'address']
