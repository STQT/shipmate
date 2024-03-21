from django.db import models


class Provider(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    class TypeChoices(models.TextChoices):
        STANDARD = "standard", "Standard"
        EXCLUSIVE = "exclusive", "Exclusive"

    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.INACTIVE)
    type = models.CharField(max_length=50, choices=TypeChoices.choices, default=TypeChoices.EXCLUSIVE)
    # TODO: add included users M:M field for leads adding
    email = models.EmailField()
    subject = models.CharField(max_length=320)
    is_external = models.BooleanField(default=True)


class ProviderLog(models.Model):
    provider = models.ForeignKey("Provider", on_delete=models.CASCADE, related_name="logs")
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.TextField()
    message = models.TextField(blank=True, null=True)
