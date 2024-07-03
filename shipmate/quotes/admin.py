from django.contrib import admin

from shipmate.quotes.models import Quote, QuoteAttachment, QuoteVehicles, QuoteLog


class QuoteLogInline(admin.TabularInline):
    model = QuoteLog
    extra = 0


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    autocomplete_fields = ["customer", "origin", "destination", "created_at"]
    list_display = ['id', 'status', 'guid']
    list_filter = ['status']
    inlines = [QuoteLogInline]
    search_fields = ['id', ]


@admin.register(QuoteAttachment)
class QuoteAttachmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'quote', 'link']
    autocomplete_fields = ['quote']


@admin.register(QuoteVehicles)
class QuoteVehiclesAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'vehicle_year', 'quote']
    autocomplete_fields = ['vehicle', 'quote']
