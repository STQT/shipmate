from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from shipmate.contrib.logging import log_update, store_old_values
from shipmate.quotes.models import Quote, QuoteLog


@receiver(pre_save, sender=Quote)
def log_store_quote_data(sender, instance, **kwargs):
    store_old_values(sender, instance, **kwargs)


@receiver(post_save, sender=Quote)
def log_quote_update(sender, instance, created, **kwargs):
    log_update(sender, instance, created, QuoteLog, "quote", **kwargs)
