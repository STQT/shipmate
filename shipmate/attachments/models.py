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
    text = models.TextField(null=True, blank=True)
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

    class StatusChoice(models.TextChoices):
        ALL = "all", "All"
        SUPPORT = "support", "Support"
        COMPLETED = "completed", "Completed"
        ARCHIVED = "archived", "Archived"

    class PriorityChoices(models.TextChoices):
        HIGH = "high", "High"
        MEDIUM = "medium", "Medium"
        LOW = "low", "Low"

    class BusyChoices(models.TextChoices):
        BUSY = "busy", "Busy"
        FREE = "free", "Free"

    type = models.CharField(max_length=10, choices=TypeChoices.choices)
    priority = models.CharField(max_length=10, choices=PriorityChoices.choices)
    busy = models.CharField(max_length=10, choices=BusyChoices.choices)
    status = models.CharField(max_length=15, choices=StatusChoice.choices, default=StatusChoice.SUPPORT)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    date = models.DateField(null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)

    class Meta:
        default_related_name = "task_attachments"


class PhoneAttachment(BaseModel):
    from_phone = models.CharField()
    to_phone = ArrayField(models.CharField(max_length=20), blank=True)

    class Meta:
        default_related_name = "phone_attachments"


class EmailAttachment(BaseModel):
    from_email = models.EmailField()
    to_email = ArrayField(models.EmailField(), blank=True)
    cc_email = ArrayField(models.EmailField(), blank=True, default=list)
    bcc_email = ArrayField(models.EmailField(), blank=True, default=list)
    subject = models.CharField(max_length=320)

    class Meta:
        default_related_name = "email_attachments"


class FileAttachment(BaseModel):
    file = models.FileField(upload_to=upload_to)

    class Meta:
        default_related_name = "file_attachments"
