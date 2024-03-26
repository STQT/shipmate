from django.contrib import admin

from shipmate.leads.models import Leads, LeadsAttachment


@admin.register(Leads)
class LeadsAdmin(admin.ModelAdmin):
    autocomplete_fields = ["origin", "destination", "customer", "vehicle"]
    ordering = ["-id"]
    list_display = ["customer", "status", "vehicle", "price"]


@admin.register(LeadsAttachment)
class LeadsAttachmentAdmin(admin.ModelAdmin):
    ...
