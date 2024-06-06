from django.apps import AppConfig


class LeadsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shipmate.leads"

    def ready(self):
        try:
            import shipmate.leads.signals  # noqa: F401
        except ImportError:
            pass
