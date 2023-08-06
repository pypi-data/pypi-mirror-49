import ast
import sys
import copy
import difflib
import time
import queue

import astunparse

from pyimprove.test_wrapper import TestWrapper
from pyimprove.edits.helpers import apply_edits
from pyimprove.search import BreadthFirstSearch

if __name__ == "__main__":
    # A minimal example of how the classes can be used.
    source_filename = sys.argv[1]
    test_filename = sys.argv[2]

    source_code = open(source_filename).read()
    tree = ast.parse(source_code)

    input_contents = astunparse.unparse(tree)
    print(input_contents)

    test_wrapper = TestWrapper(test_filename)

    search = BreadthFirstSearch(tree, test_wrapper)

    tic = time.time()
    best_patch, best_result = search.run()
    toc = time.time()

    print(best_patch, best_result)

    output_contents = astunparse.unparse(apply_edits(tree, best_patch))
    print(output_contents)

    diff = difflib.unified_diff(input_contents, output_contents)

    print()
    print("".join(diff))

    print(f"Completed in {search.evaluations} steps")
    print(f"Completed within {toc - tic} seconds")
