import datetime

from django.contrib.auth import get_user_model
from django.db import models

from shipmate.utils.models import BaseLog

User = get_user_model()


class Provider(models.Model):
    class ProviderStatusChoices(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    class ProviderEffectiveChoices(models.TextChoices):
        YES = "yes", "Yes"
        NO = "no", "No"

    class ProviderTypeChoices(models.TextChoices):
        STANDARD = "standard", "Standard"
        EXCLUSIVE = "exclusive", "Exclusive"

    name = models.CharField(max_length=255)
    status = models.CharField(max_length=8,
                              choices=ProviderStatusChoices.choices,
                              default=ProviderStatusChoices.INACTIVE)
    type = models.CharField(max_length=9, choices=ProviderTypeChoices.choices)
    effective = models.CharField(max_length=3, choices=ProviderEffectiveChoices.choices)
    leads_in_queue = models.PositiveSmallIntegerField(null=True, blank=True)
    exclusive_users = models.ManyToManyField(User, related_name='providers', blank=True)
    effective_users_count = models.PositiveSmallIntegerField(null=True, blank=True)
    email = models.EmailField()
    subject = models.CharField(max_length=320)
    value = models.FloatField(null=True, blank=True)
    default_deposit = models.FloatField(null=True, blank=True)
    is_external = models.BooleanField(default=True)
    updated_from = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="+",
                                     null=True, blank=True)

    def __str__(self):
        return self.name


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

    class DistributionStatusChoices(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    # TODO: add dynamic data for received_today and queue_now
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="distribution", editable=False)
    multiple = models.FloatField(default=DistributionMultipleChoices.S1P0,
                                 choices=DistributionMultipleChoices.choices)
    start_hour = models.TimeField(default=datetime.time(0, 0))
    finish_hour = models.TimeField(default=datetime.time(11, 59))
    status = models.CharField(max_length=8,
                              choices=DistributionStatusChoices.choices,
                              default=DistributionStatusChoices.INACTIVE)
    updated_from = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="+",
                                     null=True, blank=True)

    def __str__(self):
        return self.user


class DistributionLog(BaseLog):
    distribution = models.ForeignKey("Distribution", on_delete=models.CASCADE, related_name="logs")
