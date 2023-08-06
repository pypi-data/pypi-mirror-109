"""App config for limits."""

from django.apps import AppConfig
from django.utils.translation import ugettext as _


def load_limits_settings():
    """Load settings."""
    from kalabash.parameters import tools as param_tools
    from .app_settings import ParametersForm

    param_tools.registry.add("global", ParametersForm, _("Limits"))


class LimitsConfig(AppConfig):

    """App configuration."""

    name = "kalabash.limits"
    verbose_name = "Kalabash admin limits"

    def ready(self):
        load_limits_settings()

        from . import handlers  # NOQA:F401
