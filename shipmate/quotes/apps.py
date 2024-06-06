from django.apps import AppConfig


class QuotesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shipmate.quotes"

    def ready(self):
        try:
            import shipmate.quotes.signals  # noqa: F401
        except ImportError:
            pass
