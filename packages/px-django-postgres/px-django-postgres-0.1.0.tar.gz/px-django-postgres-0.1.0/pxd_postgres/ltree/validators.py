from django.core.validators import RegexValidator
from django.utils.translation import pgettext_lazy


__all__ = 'ltree_validator', 'ltree_int_validator'


ltree_validator = RegexValidator(
    r'^[A-Za-z0-9_.]*$',
    pgettext_lazy(
        'pxd_postgres',
        'Postgresql ltree is a sequence of alphanumeric characters and '
        'underscores separated by dots.',
    ),
    'invalid',
)

ltree_int_validator = RegexValidator(
    r'^[0-9.]*$',
    pgettext_lazy(
        'pxd_postgres',
        'Int ltree is a sequence of numbers separated by dots.',
    ),
    'invalid',
)
