from django.contrib import admin

from shipmate.carriers.models import Carrier


@admin.register(Carrier)
class CarrierAdmin(admin.ModelAdmin):
    autocomplete_fields = ["location"]
