import ast
import sys
import importlib
import unittest
import copy
import difflib
import os
from contextlib import contextmanager

import astunparse


# Adaptation of algorithm defined by Jonathan von Schroeder - Jan 27 '17
@contextmanager
def add_to_path(p):
    old_path = sys.path
    sys.path = sys.path[:]
    sys.path.insert(0, p)
    try:
        yield
    finally:
        sys.path = old_path


def basic_fitness_function(total, results):
    """ A basic fitness function which examines the number of non-passing tests

    Args:
        total (int): The amount of tests which have been evaluated.
        results (dict): The results from unittest.

    Returns:
        float: The fitness value.
    """
    return len(results.errors) + len(results.failures)


def mu_scalpel_fitness_function(total, results):
    """ An implementation of the muscalpel fitness function defined within literatuer

    Args:
        total (int): The amount of tests which have been evaluated.
        results (dict): The results from unittest.

    Returns:
        float: The fitness value.
    """

    # Rearranged into a minimisation problem with same characteristics
    succesful = total - (len(results.errors) + len(results.failures))
    compiled = total - len(results.failures)

    return (total * 2) - (succesful + compiled)


def genprog_fitness_function(total, results):
    """ An implementation of the genprof fitness function defined within literature

    Args:
        total (int): The amount of tests which have been evaluated.
        results (dict): The results from unittest.

    Returns:
        float: The fitness value.
    """

    # Same landscape as the basic one, only looking at bugs with non-seperable test cases
    return len(results.errors) + len(results.failures)


class TestWrapper:
    """ A wrapper around the test suite

    This class provides a way to test the trees by dynamically handling the module creation
    and memory management.
    """

    def __init__(self, test_filename, test_cases=0, fitness_function=basic_fitness_function):
        """ Initialization function

        Args:
            test_filename (string): The location of the test suite.
            test_cases (int): The amount of tests defined within the test suite.
            fitness_function (function): The function to be used to calculate the fitness.
        """
        self.test_filename = test_filename
        self.test_cases = test_cases
        self.fitness_function = fitness_function

        with add_to_path(os.path.dirname(self.test_filename)):
            spec = importlib.util.spec_from_file_location("", self.test_filename)

            self.test_module = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(self.test_module)

        # Silence test runner by sending to /dev/null/
        self.runner = unittest.TextTestRunner(stream=open(os.devnull, "w"))

    def run(self, tree):
        """ The main function, which returns the fitness

        Args:
            tree (Tree): The tree to be tested

        Returns:
            float: The fitness achieved by the tree.
        """
        try:
            exec(compile(tree, "<ast>", "exec"), self.test_module.__dict__)
        except ValueError:
            # Compile error!
            return sys.maxsize

        self.suite = unittest.defaultTestLoader.loadTestsFromModule(self.test_module)

        results = self.runner.run(self.suite)

        return self.fitness_function(self.test_cases, results)


if __name__ == "__main__":
    # A minimal example of how the classes can be used.

    source_filename = sys.argv[1]
    test_filename = sys.argv[2]

    source_code = open(source_filename).read()
    tree = ast.parse(source_code)

    test_wrapper = TestWrapper(test_filename)
