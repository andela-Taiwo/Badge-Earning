from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = "badge_earning.api"

    def ready(self):
        try:
            import badge_earning.api.signals  # noqa F401
        except ImportError:
            pass
