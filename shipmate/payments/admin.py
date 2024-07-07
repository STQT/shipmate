from django.contrib import admin

from shipmate.payments.models import OrderPayment


@admin.register(OrderPayment)
class OrderPaymentAdmin(admin.ModelAdmin):
    ...
