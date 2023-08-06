import ast
import os
import shutil
import subprocess
import re
import code
import unittest
import random
import copy
import math
import difflib
import importlib.util
import sys


def id_generator():
    """ Function that provides sequential id values

    To ensure all nodes are assigned a different id, this function can be
    stored and yielded each time a new id is required.

    Yields:
        int: An auto-incrementing integer
    """

    i = 0
    while True:
        yield i
        i += 1


class IdAssigner(ast.NodeTransformer):
    """ The id assigner

    This class defines a deterministic way to assign id values to each node
    within a tree. A tree that is passed to this function will always be
    returned with the same assigmented.
    """
    def __init__(self, *args, **kwargs):
        """ Initialization function """
        super(IdAssigner, self).__init__(*args, **kwargs)

        self.id_generator = id_generator()

    def generic_visit(self, node):
        """ The visit function which is called upon each node

        Args:
            node (Node): The node to be parsed.

        Returns:
            Node: The node to be updated within the tree.
        """

        if not hasattr(node, 'unique_id'):
            # Has to be copied to avoid assigning two nodes with the same value
            # due to the underlying system saving memory.
            node = copy.deepcopy(node)
            node.unique_id = next(self.id_generator)

        return super().generic_visit(node)


if __name__ == "__main__":
    # A minimal example of how the class can be used.

    source_code = open('./quixbugs/bitcount.py').read()
    tree = ast.parse(source_code)

    nodes = []
    patches = []

    idAssigner = IdAssigner()

    idAssigner.visit(tree)
