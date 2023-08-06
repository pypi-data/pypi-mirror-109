from typing import Type
from django.db.models.fields import TextField
from django.forms.widgets import TextInput

from .value import LtreeValueParserables, LtreeValue, LtreeIntValue
from .validators import ltree_validator, ltree_int_validator
from .forms import LtreeFormField, LtreeIntFormField


__all__ = (
    'LtreeValueProxy',
    'LtreeField',
    'LtreeIntValueProxy',
    'LtreeIntField',
)


class LtreeValueProxy:
    _value_type: Type[LtreeValue] = LtreeValue

    def __init__(self, field_name: str) -> None:
        self.field_name = field_name

    def __get__(self, instance, owner):
        if instance is None:
            return self

        value = instance.__dict__[self.field_name]

        if value is None:
            return value

        return self._value_type(instance.__dict__[self.field_name])

    def __set__(self, instance, value):
        if instance is None:
            return self

        instance.__dict__[self.field_name] = value


class LtreeField(TextField):
    default_validators = [ltree_validator]
    _value_type: Type[LtreeValue] = LtreeValue
    _value_proxy_type: Type[LtreeValueProxy] = LtreeValueProxy
    _form_class = LtreeFormField
    _widget = TextInput

    def db_type(self, connection):
        return 'ltree'

    def formfield(self, **kwargs):
        kwargs['form_class'] = self._form_class
        kwargs['widget'] = self._widget()
        return super(LtreeField, self).formfield(**kwargs)

    def contribute_to_class(self, cls, name, private_only=False):
        super(LtreeField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, self._value_proxy_type(self.name))

    def from_db_value(self, value, expression, connection, *args):
        if value is None:
            return value
        return self._value_type(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        return str(self._value_type(value))

    def to_python(self, value):
        if value is None:
            return value
        elif isinstance(value, self._value_type):
            return value

        return self._value_type(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return value
        elif isinstance(value, self._value_type):
            return str(value)
        elif isinstance(value, LtreeValueParserables):
            return str(self._value_type(value))

        raise ValueError('Unknown value type {}'.format(type(value)))


class LtreeIntValueProxy(LtreeValueProxy):
    _value_type: Type[LtreeIntValue] = LtreeIntValue


class LtreeIntField(LtreeField):
    default_validators = [ltree_int_validator]
    _value_type: Type[LtreeIntValue] = LtreeIntValue
    _value_proxy_type: Type[LtreeIntValueProxy] = LtreeIntValueProxy
    _form_class = LtreeIntFormField
