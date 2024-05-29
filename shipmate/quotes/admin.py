from django.contrib import admin

from shipmate.quotes.models import Quote, QuoteAttachment, QuoteVehicles


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    autocomplete_fields = ["customer", "origin", "destination"]
    list_display = ['id', 'status']
    list_filter = ['status']



@admin.register(QuoteAttachment)
class QuoteAttachmentAdmin(admin.ModelAdmin):
    ...


@admin.register(QuoteVehicles)
class QuoteVehiclesAdmin(admin.ModelAdmin):
    ...
