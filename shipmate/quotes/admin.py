from django.contrib import admin

from shipmate.quotes.models import Quote, QuoteAttachment


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    ...


@admin.register(QuoteAttachment)
class QuoteAttachmentAdmin(admin.ModelAdmin):
    ...
