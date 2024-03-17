from django.contrib import admin

from shipmate.mails.models import Mail


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    ...
