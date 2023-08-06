from django.apps import AppConfig
from django.utils.translation import pgettext_lazy


__all__ = ('PostgresConfig',)


class PostgresConfig(AppConfig):
    name = 'pxd_postgres'
    verbose_name = pgettext_lazy('pxd_postgres', 'Postgresql utils')
