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
    """A temporary type used during inference"""

    _next_free = 1  # Next free papaki.

    def __init__(self, node, spec_type=None):
        """
        Construct a new temporary type for node `node`.

        The user may optionally define the type of this node.
        """
        self.node = node
        self.inferred_type = spec_type

        self.tag = TempType._next_free
        TempType._next_free += 1

    def write_back(self):
        self.node.type = self.inferred_type
        # TODO: Validate the type before returning.


class Constraint:
    """
    A type constraint.

    Subclasses specify what kind of constraint this one really is.
    """
    pass


class SpecConstraint(Constraint):
    """
    A constraint enforcing a node to acquire a specific type.
    """

    def __init__(self, node, spec_type):
        self.node = node
        self.spec_type = spec_type


class SetConstraint(Constraint):
    """
    A constraint enforcing a node to acquire a type from a set of types.

    These constraints are due to the type system.

    Note: This is actually only used in comparison operators.
    """

    def __init_(self, node, good_types):
        self.node = node
        self.good_types = good_types


class NegSetConstraint(Constraint):
    """
    A constraint forbidding a node from acquring certain types.

    These constraints are due to the type system.
    """

    def __init_(self, node, bad_types):
        self.node = node
        self.bad_types = bad_types


class AsTypeOfConstraint(Constraint):
    """
    A constraint enforcing two nodes to have the same type.

    See the Haskell Prelude for hints.
    """

    def __init_(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
