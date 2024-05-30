from django.contrib.auth import get_user_model  # noqa
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from shipmate.contrib.logging import log_update, store_old_values
from shipmate.contrib.models import UserLog
from shipmate.users.models import Team, TeamLog, Role, RoleLog, FeatureLog, Feature

User = get_user_model()


@receiver(pre_save, sender=User)
def log_store_user_data(sender, instance, **kwargs):
    store_old_values(sender, instance, **kwargs)


@receiver(post_save, sender=User)
def log_user_update(sender, instance, created, **kwargs):
    log_update(sender, instance, created, UserLog, "user", **kwargs)


@receiver(pre_save, sender=Team)
def log_store_team_data(sender, instance, **kwargs):
    store_old_values(sender, instance, **kwargs)


@receiver(post_save, sender=Team)
def log_team_update(sender, instance, created, **kwargs):
    log_update(sender, instance, created, TeamLog, "team", **kwargs)


@receiver(pre_save, sender=Role)
def log_store_role_data(sender, instance, **kwargs):
    store_old_values(sender, instance, **kwargs)


@receiver(post_save, sender=Role)
def log_role_update(sender, instance, created, **kwargs):
    log_update(sender, instance, created, RoleLog, "role", **kwargs)


@receiver(pre_save, sender=Feature)
def log_store_feature_data(sender, instance, **kwargs):
    store_old_values(sender, instance, **kwargs)


@receiver(post_save, sender=Feature)
def log_feature_update(sender, instance, created, **kwargs):
    log_update(sender, instance, created, FeatureLog, "feature", **kwargs)
