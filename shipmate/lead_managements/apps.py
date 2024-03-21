from django.apps import AppConfig


class LeadManagementsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shipmate.lead_managements"

    def ready(self):
        try:
            import shipmate.lead_managements.signals  # noqa: F401
        except ImportError:
            pass
