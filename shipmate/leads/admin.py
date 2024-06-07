from django.contrib import admin

from shipmate.leads.models import Leads, LeadsAttachment, LeadVehicles, LeadsLog


class LeadsLogInline(admin.TabularInline):
    model = LeadsLog
    extra = 0


@admin.register(Leads)
class LeadsAdmin(admin.ModelAdmin):
    autocomplete_fields = ["origin", "destination", "customer", ]
    ordering = ["-id"]
    list_display = ["customer", "status", "price"]
    inlines = [LeadsLogInline]
    search_fields = ['id', ]


@admin.register(LeadsAttachment)
class LeadsAttachmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'lead']
    autocomplete_fields = ['lead']


@admin.register(LeadVehicles)
class LeadVehiclesAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'vehicle_year', 'lead']
    autocomplete_fields = ['vehicle', 'lead']
