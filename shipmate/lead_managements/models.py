import datetime

from django.contrib.auth import get_user_model
from django.db import models

from shipmate.contrib.models import BaseLog

User = get_user_model()


class Provider(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_exclusive = models.BooleanField(default=False)  # NOTE: for field exclusive_users
    is_effective = models.BooleanField(default=False)  # NOTE: for field effective_users_count
    exclusive_users = models.ManyToManyField(User, related_name='providers', blank=True)
    effective_users_count = models.PositiveSmallIntegerField(null=True, blank=True)
    email = models.EmailField()
    subject = models.CharField(max_length=320)
    is_external = models.BooleanField(default=True)
    updated_from = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="provider_updates",
                                     null=True, blank=True)


class ProviderLog(BaseLog):
    provider = models.ForeignKey("Provider", on_delete=models.CASCADE, related_name="logs")


class Distribution(models.Model):
    class DistributionMultipleChoices(models.TextChoices):
        S0P5 = 0.5, '0.5X'
        S1P0 = 1.0, '1X'
        S1P5 = 1.5, '1.5X'
        S2P0 = 2.0, '2X'
        S2P5 = 2.5, '2.5X'
        S3P0 = 3.0, '3X'
    # TODO: add dynamic data for received_today and queue_now
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="distribution", editable=False)
    multiple = models.FloatField(default=DistributionMultipleChoices.S1P0,
                                 choices=DistributionMultipleChoices.choices)
    start_hour = models.TimeField(default=datetime.time(0, 0))
    finish_hour = models.TimeField(default=datetime.time(11, 59))
    is_active = models.BooleanField(default=False)
    updated_from = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="distribution_updates",
                                     null=True, blank=True)


class DistributionLog(BaseLog):
    distribution = models.ForeignKey("Distribution", on_delete=models.CASCADE, related_name="logs")
