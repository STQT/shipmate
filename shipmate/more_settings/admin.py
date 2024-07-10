from django.contrib import admin
from django.contrib.auth import get_user_model

from shipmate.more_settings.models import AutomationLog, Automation

User = get_user_model()


class AutomationLogInline(admin.TabularInline):
    model = AutomationLog
    extra = 0


@admin.register(Automation)
class AutomationAdmin(admin.ModelAdmin):
    inlines = [AutomationLogInline]
