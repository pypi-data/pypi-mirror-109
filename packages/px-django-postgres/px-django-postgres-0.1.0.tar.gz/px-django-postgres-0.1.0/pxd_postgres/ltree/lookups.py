from django.db.models import Lookup, Transform, IntegerField

from .fields import LtreeField


__all__ = (
    'EqualLookup',
    'AncestorLookup',
    'DescendantLookup',
    'MatchLookup',
    'ContainsLookup',

    'DepthTransform',
)


class SimpleLookup(Lookup):
    lookup_operator: str = '='

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = list(lhs_params) + list(rhs_params)
        return '{} {} {}'.format(lhs, self.lookup_operator, rhs), params


@LtreeField.register_lookup
class EqualLookup(SimpleLookup):
    lookup_name: str = 'exact'
    lookup_operator: str = '='


@LtreeField.register_lookup
class AncestorLookup(SimpleLookup):
    lookup_name: str = 'ancestor'
    lookup_operator: str = '@>'


@LtreeField.register_lookup
class DescendantLookup(SimpleLookup):
    lookup_name: str = 'descendant'
    lookup_operator: str = '<@'


@LtreeField.register_lookup
class MatchLookup(SimpleLookup):
    lookup_name: str = 'match'
    lookup_operator: str = '~'


@LtreeField.register_lookup
class ContainsLookup(SimpleLookup):
    lookup_name: str = 'contains'
    lookup_operator: str = '?'


@LtreeField.register_lookup
class DepthTransform(Transform):
    lookup_name = 'depth'
    function = 'nlevel'

    @property
    def output_field(self):
        return IntegerField()
