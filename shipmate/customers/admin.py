from django.contrib import admin
from .models import ExternalContacts, Customer


class ExternalContactsInline(admin.TabularInline):
    model = ExternalContacts
    extra = 1


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    inlines = [ExternalContactsInline]
    search_fields = ["name", "phone", "email", "last_name"]
    list_display = ["name", "last_name", "phone", "email"]
    ordering = ["-id"]
