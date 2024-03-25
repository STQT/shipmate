from django.contrib import admin

from shipmate.orders.models import Order, OrderAttachment


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    ...


@admin.register(OrderAttachment)
class OrderAttachmentAdmin(admin.ModelAdmin):
    ...
