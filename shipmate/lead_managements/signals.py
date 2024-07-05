from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Provider, ProviderLog, Distribution, DistributionLog
from ..contrib.logging import log_update, store_old_values

User = get_user_model()


@receiver(pre_save, sender=Provider)
def log_store_user_data(sender, instance, **kwargs):
    store_old_values(sender, instance, **kwargs)


@receiver(post_save, sender=Provider)
def log_provider_update(sender, instance, created, **kwargs):
    log_update(sender, instance, created, ProviderLog, "provider", **kwargs)


@receiver(post_save, sender=User)
def create_user_distribution(sender, instance, created, **kwargs):
    if created:
        Distribution.objects.create(user=instance)


@receiver(pre_save, sender=Distribution)
def log_store_distribution_data(sender, instance, **kwargs):
    store_old_values(sender, instance, **kwargs)


@receiver(post_save, sender=Distribution)
def log_distribution_update(sender, instance, created, **kwargs):
    log_update(sender, instance, created, DistributionLog, "distribution", **kwargs)
