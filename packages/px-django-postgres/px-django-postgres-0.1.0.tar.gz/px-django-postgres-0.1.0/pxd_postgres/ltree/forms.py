from django.forms import CharField

from .validators import ltree_validator, ltree_int_validator


__all__ = 'LtreeFormField', 'LtreeIntFormField',


class LtreeFormField(CharField):
    default_validators = [ltree_validator]


class LtreeIntFormField(CharField):
    default_validators = [ltree_int_validator]
