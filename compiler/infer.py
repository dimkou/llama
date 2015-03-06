"""
# ----------------------------------------------------------------------
# infer.py
#
# Type inference for Llama
# http://courses.softlab.ntua.gr/compilers/2012a/llama2012.pdf
#
# Authors: Nick Korasidis <renelvon@gmail.com>
#          Dimitris Koutsoukos <dim.kou.shmmy@gmail.com>
# ----------------------------------------------------------------------
"""


class TempType:
    """A temporary type used during inference."""

    _next_free = 1  # Next free papaki.

    @classmethod
    def _get_next_tag(cls):
        cls._next_free += 1
        return cls._next_free

    def __init__(self, node, spec_type=None):
        """
        Construct a new temporary type for node `node`.

        The user may optionally supply a type for this node;
        such a specification is not binding but will improve
        error reporting.
        """
        self._node = node
        self._spec_type = spec_type
        self._inferred_type = None

        self._tag = self._get_next_tag()

    def write_back(self):
        self._node.type = self._inferred_type
        # TODO: Validate the type before returning.


class Constraint:
    """
    A type constraint.

    Subclasses specify what kind of constraint this one really is.
    """
    pass


class SpecConstraint(Constraint):
    """
    A constraint enforcing a TempType to acquire a specific type.
    """

    def __init__(self, ttype, spec_type):
        self.ttype = ttype
        self.spec_type = spec_type


class SetConstraint(Constraint):
    """
    A constraint enforcing a TempType to acquire a value from a given set.

    These constraints are due to the type system.

    Note: This is actually only used in comparison operators.
    """

    def __init__(self, ttype, good_types):
        self.ttype = ttype
        self.good_types = good_types


class NegSetConstraint(Constraint):
    """
    A constraint forbidding a TempType from acquring certain types.

    These constraints are due to the type system.
    """

    def __init__(self, ttype, bad_types):
        self.ttype = ttype
        self.bad_types = bad_types


class AsTypeOfConstraint(Constraint):
    """
    A constraint enforcing two TempTypes to have the same type.

    See the Haskell Prelude for hints.
    """

    def __init__(self, ttype1, ttype2):
        self.ttype1 = ttype1
        self.ttype2 = ttype2
