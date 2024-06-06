from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from shipmate.contrib.logging import log_update, store_old_values
from shipmate.orders.models import Order, OrderLog


@receiver(pre_save, sender=Order)
def log_store_order_data(sender, instance, **kwargs):
    store_old_values(sender, instance, **kwargs)


@receiver(post_save, sender=Order)
def log_order_update(sender, instance, created, **kwargs):
    log_update(sender, instance, created, OrderLog, "order", **kwargs)
