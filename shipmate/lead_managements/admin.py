from django.contrib import admin
from .models import *


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    ...
