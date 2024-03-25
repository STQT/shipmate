from django.contrib import admin
from .models import TaskAttachment, EmailAttachment, FileAttachment, PhoneAttachment


@admin.register(TaskAttachment)
class TaskAttachmentAdmin(admin.ModelAdmin):
    ...


@admin.register(EmailAttachment)
class EmailAttachmentAdmin(admin.ModelAdmin):
    ...


@admin.register(FileAttachment)
class FileAttachmentAdmin(admin.ModelAdmin):
    ...


@admin.register(PhoneAttachment)
class PhoneAttachmentAdmin(admin.ModelAdmin):
    ...
