from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Provider, ProviderLog, Distribution, DistributionLog
from ..contrib.logging import log_update

User = get_user_model()


@receiver(post_save, sender=Provider)
def log_distribution_update(sender, instance, created, **kwargs):
    log_update(sender, instance, created, ProviderLog, "provider", **kwargs)


@receiver(post_save, sender=User)
def create_user_distribution(sender, instance, created, **kwargs):
    if created:
        Distribution.objects.create(user=instance)


@receiver(post_save, sender=Distribution)
def log_distribution_update(sender, instance, created, **kwargs):
    log_update(sender, instance, created, DistributionLog, "distribution", **kwargs)
