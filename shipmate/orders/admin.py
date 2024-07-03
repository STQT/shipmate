from django.contrib import admin

from shipmate.orders.models import Order, OrderAttachment, OrderVehicles, OrderContract


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ["customer", "origin", "destination"]
    list_display = ['id', 'status', 'guid', 'created_at']
    list_filter = ['status']
    search_fields = ['id', ]


@admin.register(OrderAttachment)
class OrderAttachmentAdmin(admin.ModelAdmin):
    autocomplete_fields = ['order']
    list_display = ['title', 'order', 'link']


@admin.register(OrderVehicles)
class OrderVehiclesAdmin(admin.ModelAdmin):
    autocomplete_fields = ['order', 'vehicle']


@admin.register(OrderContract)
class OrderContractAdmin(admin.ModelAdmin):
    list_display = ['order', 'signed', 'contract_type', 'created_at']
