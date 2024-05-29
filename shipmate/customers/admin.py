from django.contrib import admin
from .models import *


class ExternalContactsInline(admin.TabularInline):
    model = ExternalContacts
    extra = 1


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    inlines = [ExternalContactsInline]
    search_fields = ["name", "phone", "email"]
    list_display = ["name", "phone", "email"]
    ordering = ["-id"]
