from django.db import models


class Mail(models.Model):
    subject = models.CharField(max_length=255)
    sender = models.CharField(max_length=320)
    recipient = models.CharField(max_length=320)
    date = models.CharField(max_length=50)
    body = models.TextField()

    def __str__(self):
        return f"{self.sender} - {self.subject}"
