from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AccountsAppConfig(AppConfig):
    name = 'bitakora.accounts'
    verbose_name = _('User management')