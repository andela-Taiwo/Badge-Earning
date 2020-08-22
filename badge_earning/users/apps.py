from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "badge_earning.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import badge_earning.users.signals  # noqa F401
        except ImportError:
            pass
