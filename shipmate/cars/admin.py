from django.contrib import admin
from .models import CarsModel, CarMarks


@admin.register(CarsModel)
class CarsModelAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(CarMarks)
class CarMarksAdmin(admin.ModelAdmin):
    search_fields = ["name"]
