from django.contrib import admin
from .models import *


@admin.register(CarsModel)
class CarsModelAdmin(admin.ModelAdmin):
    ...


@admin.register(CarMarks)
class CarMarksAdmin(admin.ModelAdmin):
    ...
