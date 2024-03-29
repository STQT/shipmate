from django.contrib import admin

from shipmate.leads.models import Leads, LeadsAttachment


@admin.register(Leads)
class LeadsAdmin(admin.ModelAdmin):
    autocomplete_fields = ["origin", "destination", "customer",]
    ordering = ["-id"]
    list_display = ["customer", "status", "price"]


@admin.register(LeadsAttachment)
class LeadsAttachmentAdmin(admin.ModelAdmin):
    ...
