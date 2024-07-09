from django.contrib import admin

from shipmate.payments.models import OrderPayment, OrderPaymentAttachment


class OrderPaymentAttachmentInline(admin.TabularInline):
    model = OrderPaymentAttachment
    extra = 0


@admin.register(OrderPayment)
class OrderPaymentAdmin(admin.ModelAdmin):
    inlines = [OrderPaymentAttachmentInline]


@admin.register(OrderPaymentAttachment)
class OrderPaymentAttachmentAdmin(admin.ModelAdmin):
    ...
