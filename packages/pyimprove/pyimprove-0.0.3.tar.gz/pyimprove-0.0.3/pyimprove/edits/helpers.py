import random
import copy

from pyimprove.edits.id_assigner import IdAssigner

from pyimprove.edits.alter import candidate_finder as alter_candidate_finder
from pyimprove.edits.move import candidate_finder as move_candidate_finder
from pyimprove.edits.variable_swap import candidate_finder as variable_swap_candidate_finder


def get_edits(tree):
    """ Function to retrieve all edits applicable to a tree

    This function amalgamates all edit types into one helper function

    Args:
        tree (Tree): Tree to be analysed.

    Returns:
        list: Valid edits that can be applied to the tree
    """
    candidates = alter_candidate_finder(tree)
    candidates.update(move_candidate_finder(tree))
    candidates.update(variable_swap_candidate_finder(tree))

    return candidates


def get_edit(tree):
    """ Function to retrieve a random edit

    This function uses the above to wrap a random selection method, which
    can be used for stocastic methods easily.

    Args:
        tree (Tree): Tree to be analysed.

    Returns:
        Object: Valid edit that can be applied
    """
    candidates = get_edits(tree)

    return random.choices(population=list(candidates), weights=candidates.values())[0]


def apply_edits(tree, edits):
    """ Function that applys a sequential list of edits

    Each edit requires a further traversal of the tree to ensure all nodes
    are annotated with an id. This function does so, providing a consice
    helper function.

    Args:
        tree (Tree): Tree to be edited.
        edits (list): List of edits to be applied to the tree.

    Returns:
        Tree: The new tree
    """
    tree = copy.deepcopy(tree)

    id_assigner = IdAssigner()
    tree = id_assigner.visit(tree)

    for edit in edits:
        tree = edit.apply(tree)
        tree = id_assigner.visit(tree)

    return tree
