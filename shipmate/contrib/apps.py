from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ContribConfig(AppConfig):
    name = "shipmate.contrib"
    verbose_name = _("Contrib")
