from django.apps import AppConfig


class CompanyManagementConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shipmate.company_management"

    def ready(self):
        try:
            import shipmate.company_management.signals  # noqa: F401
        except ImportError:
            pass
