from django.contrib.auth import get_user_model
from django.db import models

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


class ProviderLog(models.Model):
    provider = models.ForeignKey("Provider", on_delete=models.CASCADE, related_name="logs")
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.TextField()
    message = models.TextField(blank=True, null=True)
