from django.apps import AppConfig
from django.utils.translation import pgettext_lazy


__all__ = ('LtreeConfig',)


class LtreeConfig(AppConfig):
    name = 'pxd_postgres.ltree'
    label = 'pxd_postgres_ltree'
    verbose_name = pgettext_lazy('pxd_postgres:ltree', 'Postgresql ltree utils')
