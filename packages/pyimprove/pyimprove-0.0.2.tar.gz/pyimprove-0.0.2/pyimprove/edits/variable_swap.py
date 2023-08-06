import ast
import random


class CandidateApplier(ast.NodeTransformer):
    """ A candidate applier for the variable swap edit type

    This class applys a swap edit to a tree by finding
    the node and swapping the variable for another within the program.
    """

    def __init__(self, candidate, *args, **kwargs):
        """ Initialization function

        Args:
            candidate (VariableSwapEdt): The edit to be applied.
        """

        super(CandidateApplier, self).__init__(*args, **kwargs)

        self.candidate = candidate

    def generic_visit(self, node):
        """ The visit function which is called upon each node

        Args:
            node (Node): The node to be parsed.

        Returns:
            Node: The node to be updated within the tree.
        """
        if node.unique_id == self.candidate.unique_id:
            node.id = self.candidate.new_id

            return node
        return super().generic_visit(node)


class VariableSwapEdit:
    """ The variable swap edit

    This class defines a swap edit which
    swaps a variable name for another within the program.
    """

    def __init__(self, unique_id, new_id):
        """ Initialization function

        Args:
            unique_id (int): The node's id.
            new_id (int): The new id of the node.
        """
        self.unique_id = unique_id
        self.new_id = new_id

    def apply(self, tree):
        """ The application function

        Args:
            tree (Tree): The tree to which the edit should be applied.

        Returns:
            Tree: The tree with the edit applied.
        """
        return CandidateApplier(self).visit(tree)


def candidate_finder(tree):
    """ The function to find candidates

    This function can be given an arbitrary tree and return a list of edits
    and their corresponding weightings which are used to select from.

    Args:
        tree (Tree): Tree to be analysed.

    Returns:
        list: Valid edits that can be applied to the tree
    """

    # All weights are defined statically as there are no variations of the edits
    static_weight = 1

    ids = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id not in ids:
            ids.append(node.id)

    # Try and find 'activtion sites' for mutation
    candidates = {}

    # Go through every node
    for node in ast.walk(tree):
        # Go through all different mutation node types
        if isinstance(node, ast.Name):
            # We can apply this template to this node, make a reference
            for id in ids:
                if node.id != id:
                    candidates[VariableSwapEdit(node.unique_id, id)] = static_weight

    return candidates
