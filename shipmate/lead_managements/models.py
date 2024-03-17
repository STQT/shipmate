from django.db import models


class Provider(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        ARCHIVE = "archive", "Archive"

    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.INACTIVE)
    # TODO: continue
