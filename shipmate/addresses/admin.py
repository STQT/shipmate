from django.contrib import admin
from .models import States, City


@admin.register(States)
class StatesAdmin(admin.ModelAdmin):
    search_fields = ["name", "code"]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ["name", "state", "zip", "long", "lat"]
    search_fields = ["name"]
