import os
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.postgres.fields import ArrayField

from shipmate.customers.models import Customer

User = get_user_model()


def upload_to(instance, filename):
    now = datetime.now()
    path = f"{now.year}/{now.month:02d}/{now.day:02d}"
    return os.path.join(path, filename)


class BaseModel(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        abstract = True


class NoteAttachment(BaseModel):
    class Meta:
        default_related_name = "note_attachments"


class TaskAttachment(BaseModel):
    class TypeChoices(models.TextChoices):
        CALL = "call", "Call"
        EMAIL = "email", "Email"
        TASK = "task", "Task"
        DEADLINE = "deadline", "Deadline"
        PAYMENT = "payment", "Payment"

    type = models.CharField(max_length=10, choices=TypeChoices.choices)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)

    class Meta:
        default_related_name = "task_attachments"


class PhoneAttachment(BaseModel):
    from_phone = models.CharField()
    to_phone = ArrayField(models.CharField(max_length=20), blank=True)

    class Meta:
        default_related_name = "phone_attachments"


class EmailAttachment(BaseModel):
    from_email = models.CharField()
    to_email = ArrayField(models.CharField(max_length=20), blank=True)
    subject = models.CharField(max_length=320)

    class Meta:
        default_related_name = "email_attachments"


class FileAttachment(BaseModel):
    file = models.FileField(upload_to=upload_to)

    class Meta:
        default_related_name = "file_attachments"