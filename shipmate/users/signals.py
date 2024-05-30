from django.contrib.auth import get_user_model # noqa
from django.db.models.signals import post_save
from django.dispatch import receiver

from shipmate.contrib.logging import log_update
from shipmate.contrib.models import UserLog

User = get_user_model()


@receiver(post_save, sender=User)
def log_user_update(sender, instance, created, **kwargs):
    print("HERE")
    log_update(sender, instance, created, UserLog, "user", **kwargs)
