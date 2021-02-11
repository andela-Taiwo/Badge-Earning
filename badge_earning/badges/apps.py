from django.apps import AppConfig


class BadgesConfig(AppConfig):
    name = "badge_earning.badges"

    def ready(self):
        try:
            import badge_earning.badges.signals  # noqa F401
        except ImportError:
            pass
