from django.db import models


class BaseLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.TextField()
    message = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ["-id"]
