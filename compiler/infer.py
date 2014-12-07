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
        self.inferred_type = user_type

        self.tag = TempType._next_free
        TempType._next_free += 1

    def write_back(self):
        self.node.type = self.inferred_type
        # TODO: Validate the type before returning.
