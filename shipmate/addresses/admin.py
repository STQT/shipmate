from django.contrib import admin
from .models import *


@admin.register(States)
class StatesAdmin(admin.ModelAdmin):
    ...


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ["name", "state", "zip", "long", "lat"]
