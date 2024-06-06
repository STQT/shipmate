from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shipmate.orders"

    def ready(self):
        try:
            import shipmate.orders.signals  # noqa: F401
        except ImportError:
            pass
