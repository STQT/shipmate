from django.contrib import admin

from shipmate.leads.models import Leads


@admin.register(Leads)
class LeadsAdmin(admin.ModelAdmin):
    ...
