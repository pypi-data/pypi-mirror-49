import ast
import random


class CandidateApplier(ast.NodeTransformer):
    """ A candidate applier for the move edit type

    This class applys a move edit to a tree by finding
    the from node, to node, and performing the move.
    """
    def __init__(self, candidate, *args, **kwargs):
        """ Initialization function

        Args:
            candidate (MoveEdit): The edit to be applied.
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
            if self.candidate.swap:
                first_element = node.body[self.candidate.from_index]
                second_element = node.body[self.candidate.to_index]

                node.body[self.candidate.from_index] = second_element
                node.body[self.candidate.to_index] = second_element
            else:
                element = node.body.pop(self.candidate.from_index)
                node.body.insert(self.candidate.to_index, element)

            return node

        return super().generic_visit(node)


class MoveEdit:
    """ The move edit

    This class defines an movement edit which
    moves a node within the tree.
    """
    def __init__(self, unique_id, from_index, to_index, swap):
        """ Initialization function

        Args:
            unique_id (int): The node's id.
            from_index (int): The from id.
            to_index (int): The to id.
            swap (boolean): Whether the nodes should be swapped or moved.
        """
        self.unique_id = unique_id
        self.from_index = from_index
        self.to_index = to_index
        self.swap = swap

    def apply(self, tree):
        """ The application function

        Args:
            tree (Tree): The tree to which the edit should be applied.

        Returns:
            Tree: The tree with the edit applied.
        """
        return CandidateApplier(self).visit(tree)


class MoveTemplate:
    """ The move template

    This class defines a template for which a move
    can be applied to the tree.
    """
    def __init__(self, statement_type, swap, weight):
        """ Initialization function

        Args:
            statement_type (Object): The type of statement to which the edit can be applied to.
            swap (Boolean): The resultant object after the edit.
            weight (float): Whether the nodes should be swapped or moved.
        """
        self.statement_type = statement_type
        self.swap = swap
        self.weight = weight


# Defines the global list of templates to be used within the search algorithm
templates = []

templates.append(MoveTemplate(ast.FunctionDef, True, 1))
templates.append(MoveTemplate(ast.FunctionDef, False, 1))


def candidate_finder(tree, templates=templates):
    """ The function to find candidates

    This function can be given an arbitrary tree and return a list of edits
    and their corresponding weightings which are used to select from.

    Args:
        tree (Tree): Tree to be analysed.
        templates (list): Input value to be mapped.

    Returns:
        list: Valid edits that can be applied to the tree
    """

    # Try and find 'activtion sites' for mutation
    candidates = {}

    # Go through every node
    for node in ast.walk(tree):
        # Go through all different mutation node types
        for template in templates:
            # If the current node is the same or a subclass of it
            if isinstance(node, template.statement_type) and len(node.body) > 1:
                # We can apply this template to this node, make a reference
                for from_index in range(len(node.body)):
                    for to_index in range(len(node.body)):
                        if from_index == to_index:
                            if template.swap:
                                break
                            else:
                                continue

                        candidates[MoveEdit(node.unique_id, from_index, to_index, template.swap)] = template.weight

    return candidates
