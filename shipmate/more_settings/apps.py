from django.apps import AppConfig


class MoreSettingsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shipmate.more_settings"

    def ready(self):
        try:
            import shipmate.more_settings.signals  # noqa: F401
        except ImportError:
            pass
