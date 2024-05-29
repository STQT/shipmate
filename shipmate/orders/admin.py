from django.contrib import admin

from shipmate.orders.models import Order, OrderAttachment, OrderVehicles


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ["customer", "origin", "destination"]
    list_display = ['id', 'status']
    list_filter = ['status']
    search_fields = ['id', ]


@admin.register(OrderAttachment)
class OrderAttachmentAdmin(admin.ModelAdmin):
    autocomplete_fields = ['order']


@admin.register(OrderVehicles)
class OrderVehiclesAdmin(admin.ModelAdmin):
    autocomplete_fields = ['order', 'vehicle']
