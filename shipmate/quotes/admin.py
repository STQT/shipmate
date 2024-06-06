from django.contrib import admin

from shipmate.quotes.models import Quote, QuoteAttachment, QuoteVehicles, QuoteLog


class QuoteLogInline(admin.TabularInline):
    model = QuoteLog
    extra = 0


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    autocomplete_fields = ["customer", "origin", "destination"]
    list_display = ['id', 'status']
    list_filter = ['status']
    inlines = [QuoteLogInline]



@admin.register(QuoteAttachment)
class QuoteAttachmentAdmin(admin.ModelAdmin):
    ...


@admin.register(QuoteVehicles)
class QuoteVehiclesAdmin(admin.ModelAdmin):
    ...
