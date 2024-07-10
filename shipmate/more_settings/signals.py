from django.contrib.auth import get_user_model  # noqa
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from shipmate.contrib.logging import log_update, store_old_values
from shipmate.more_settings.models import Automation, AutomationLog


@receiver(pre_save, sender=Automation)
def log_store_automation_data(sender, instance, **kwargs):
    store_old_values(sender, instance, **kwargs)


@receiver(post_save, sender=Automation)
def log_automation_update(sender, instance, created, **kwargs):
    log_update(sender, instance, created, AutomationLog, "automation", **kwargs)
