import queue
import sys

from pyimprove.edits.helpers import apply_edits, get_edits


class DepthFirstSearch:
    """ A depth first implementation

    This class provides a search over the space of trees
    by applying edits, preliminary focusing on exploring improved
    solutions first.
    """

    def __init__(self, tree, test_wrapper):
        """ Initialization function

        Args:
            tree (Tree): The tree to be searched.
            test_wrapper (TestWrapper): The instance used to test the tree.
        """
        self.tree = tree
        self.test_wrapper = test_wrapper
        self.evaluations = 0

    def run(self, patch=[], best_result=sys.maxsize):
        """ The main function, which is called recursively

        Args:
            patch (list): The current list of edits.
            best_result (float): The current test result.

        Returns:
            (list, float): The best patch found, and the corresponding result.
        """

        # Get a tree up to the current state
        tree = apply_edits(self.tree, patch)

        # Get the base result
        result = self.test_wrapper.run(tree)

        self.evaluations += 1

        # If no better than the best previous, ignore further search
        if result >= best_result:
            return patch, result

        # Hit best, return now, no more exploration needed
        if result == 0:
            return patch, result

        edits = get_edits(tree)

        edits = sorted(edits.items(), key=lambda kv: kv[1])
        edits.reverse()

        candidate_patches = [patch + [edit] for edit, _ in edits]

        # For all neighbours, find best patch and result
        for candidate_patch in candidate_patches:
            final_patch, final_result = self.run(candidate_patch, result)

            if final_result < result:
                patch = final_patch
                result = final_result

        # Best combination of patch and result for this branch
        return patch, result


class BreadthFirstSearch:
    """ A breadth first implementation

    This class provides a search over the space of trees
    by applying edits, preliminary focusing on the patches closest to the
    current tree.
    """

    def __init__(self, tree, test_wrapper):
        """ Initialization function

        Args:
            tree (Tree): The tree to be searched.
            test_wrapper (TestWrapper): The instance used to test the tree.
        """
        self.tree = tree
        self.test_wrapper = test_wrapper
        self.evaluations = 0

    def run(self):
        """ The main function

        Args:
            patch (list): The current list of edits.
            best_result (float): The current test result.

        Returns:
            (list, float): The best patch found, and the corresponding result.
        """
        final_result = sys.maxsize
        final_patch = []

        self.queue = queue.Queue()
        self.queue.put((sys.maxsize, []))

        while not self.queue.empty():
            best_result, patch = self.queue.get()

            tree = apply_edits(self.tree, patch)
            result = self.test_wrapper.run(tree)

            self.evaluations += 1

            # If no better than the best previous, ignore further search
            if result >= best_result:
                continue

            # If no perfect solution found, still want to return best
            if result < final_result:
                final_result = result
                final_patch = patch

            if result == 0:
                return patch, result

            edits = get_edits(tree)

            edits = sorted(edits.items(), key=lambda kv: kv[1])
            edits.reverse()

            candidate_patches = [patch + [edit] for edit, _ in edits]

            for candidate_patch in candidate_patches:
                self.queue.put((result, candidate_patch))

        return final_patch, final_result
