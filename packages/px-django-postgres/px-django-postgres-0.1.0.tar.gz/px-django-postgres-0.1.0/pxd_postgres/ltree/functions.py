from django.db.models import Func

from .fields import LtreeField

__all__ = 'LtreeConcatFunc', 'LtreeSubpathFunc',


class LtreeConcatFunc(Func):
    function = 'ltree_concat'
    arg_joiner = ' || '
    template_postgresql = "%(expressions)s"

    def as_postgresql(self, compiler, connection):
        return self.as_sql(compiler, connection, template=self.template_postgresql)


class LtreeSubpathFunc(Func):
    function = 'subpath'

    @property
    def output_field(self):
        return LtreeField()
