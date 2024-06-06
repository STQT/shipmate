from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from shipmate.contrib.logging import log_update, store_old_values
from shipmate.leads.models import Leads, LeadsLog


@receiver(pre_save, sender=Leads)
def log_store_lead_data(sender, instance, **kwargs):
    store_old_values(sender, instance, **kwargs)


@receiver(post_save, sender=Leads)
def log_lead_update(sender, instance, created, **kwargs):
    log_update(sender, instance, created, LeadsLog, "lead", **kwargs)
