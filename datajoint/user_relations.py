"""
Hosts the table tiers, user relations should be derived from.
"""

import abc
from .relation import Relation
from .autopopulate import AutoPopulate
from .utils import from_camel_case
from . import DataJointError


class Part(Relation, metaclass=abc.ABCMeta):
    """
    Inherit from this class if the table's values are details of an entry in another relation
    and if this table is populated by this relation. For example, the entries inheriting from
    dj.Part could be single entries of a matrix, while the parent table refers to the entire matrix.
    Part relations are implemented as classes inside classes.
    """

    @property
    def master(self):
        if not hasattr(self, '_master'):
            raise DataJointError(
                'Part relations must be declared inside a base relation class')
        return self._master

    @property
    def table_name(self):
        return self.master().table_name + '__' + from_camel_case(self.__class__.__name__)


class Manual(Relation, metaclass=abc.ABCMeta):
    """
    Inherit from this class if the table's values are entered manually.
    """

    @property
    def table_name(self):
        """
        :returns: the table name of the table formatted for mysql.
        """
        return from_camel_case(self.__class__.__name__)


class Lookup(Relation, metaclass=abc.ABCMeta):
    """
    Inherit from this class if the table's values are for lookup. This is
    currently equivalent to defining the table as Manual and serves semantic
    purposes only.
    """

    @property
    def table_name(self):
        """
        :returns: the table name of the table formatted for mysql.
        """
        return '#' + from_camel_case(self.__class__.__name__)

    def _prepare(self):
        """
        Checks whether the instance has a property called `contents` and inserts its elements.
        """
        if hasattr(self, 'contents'):
            self.insert(self.contents, skip_duplicates=True)


class Imported(Relation, AutoPopulate, metaclass=abc.ABCMeta):
    """
    Inherit from this class if the table's values are imported from external data sources.
    The inherited class must at least provide the function `_make_tuples`.
    """

    @property
    def table_name(self):
        """
        :returns: the table name of the table formatted for mysql.
        """
        return "_" + from_camel_case(self.__class__.__name__)


class Computed(Relation, AutoPopulate, metaclass=abc.ABCMeta):
    """
    Inherit from this class if the table's values are computed from other relations in the schema.
    The inherited class must at least provide the function `_make_tuples`.
    """

    @property
    def table_name(self):
        """
        :returns: the table name of the table formatted for mysql.
        """
        return "__" + from_camel_case(self.__class__.__name__)