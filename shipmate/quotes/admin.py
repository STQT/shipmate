from django.contrib import admin

from shipmate.quotes.models import Quote


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    ...
