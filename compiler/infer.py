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
