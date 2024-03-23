from django.contrib import admin
from .models import *


class ExternalContactsInline(admin.TabularInline):
    model = ExternalContacts
    extra = 1


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    inlines = [ExternalContactsInline]
