from django.contrib import admin

from shipmate.leads.models import Leads, LeadsAttachment


@admin.register(Leads)
class LeadsAdmin(admin.ModelAdmin):
    ...


@admin.register(LeadsAttachment)
class LeadsAttachmentAdmin(admin.ModelAdmin):
    ...
