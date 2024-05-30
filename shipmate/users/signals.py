from django.contrib.auth import get_user_model  # noqa
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from shipmate.contrib.logging import log_update, store_old_values
from shipmate.contrib.models import UserLog

User = get_user_model()


@receiver(pre_save, sender=User)
def log_store_user_data(sender, instance, **kwargs):
    store_old_values(sender, instance, **kwargs)


@receiver(post_save, sender=User)
def log_user_update(sender, instance, created, **kwargs):
    log_update(sender, instance, created, UserLog, "user", **kwargs)
