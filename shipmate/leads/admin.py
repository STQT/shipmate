from django.contrib import admin

from shipmate.leads.models import Leads, LeadsAttachment, LeadVehicles, LeadsLog, LeadAttachmentComment


class LeadsLogInline(admin.TabularInline):
    model = LeadsLog
    extra = 0


class LeadsAttachmentCommentInline(admin.TabularInline):
    model = LeadAttachmentComment
    extra = 0


@admin.register(Leads)
class LeadsAdmin(admin.ModelAdmin):
    list_display = ["customer", "status", "price", 'user', 'guid', 'created_at']
    autocomplete_fields = ["origin", "destination", "customer"]
    ordering = ["-id"]
    inlines = [LeadsLogInline]
    search_fields = ['id', ]


@admin.register(LeadsAttachment)
class LeadsAttachmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'lead', 'link']
    autocomplete_fields = ['lead']
    inlines = [LeadsAttachmentCommentInline]


@admin.register(LeadVehicles)
class LeadVehiclesAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'vehicle_year', 'lead']
    autocomplete_fields = ['vehicle', 'lead']
