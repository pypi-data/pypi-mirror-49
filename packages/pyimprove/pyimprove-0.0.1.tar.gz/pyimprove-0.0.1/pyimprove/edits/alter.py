import ast
import random


class CandidateApplier(ast.NodeTransformer):
    """ A candidate applier for the alter edit type

    This class applys an alter edit to a tree by finding
    the applicable node and performing the alteration.
    """
    def __init__(self, candidate, *args, **kwargs):
        """ Initialization function

        Args:
            candidate (AlterEdit): The edit to be applied.
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
            Node = self.candidate.out_type

            # If delete, delete
            if Node is None:
                return

            return Node()

        return super().generic_visit(node)


class AlterEdit:
    """ The alter edit

    This class defines an alteration edit which
    changes a quality of a particular node.
    """
    def __init__(self, unique_id, out_type):
        """ Initialization function

        Args:
            unique_id (int): The node's id.
            out_type (Object): The resultant object after the edit.
        """
        self.unique_id = unique_id
        self.out_type = out_type

    def apply(self, tree):
        """ The application function

        Args:
            tree (Tree): The tree to which the edit should be applied.

        Returns:
            Tree: The tree with the edit applied.
        """
        return CandidateApplier(self).visit(tree)


class AlterTemplate:
    """ The alter template

    This class defines a template for which an alter
    can be applied to the tree.
    """
    def __init__(self, in_type, out_type, weight):
        """ Initialization function

        Args:
            in_type (Object): The object to which the edit can be applied to.
            out_type (Object): The resultant object after the edit.
            weight (float): The proportional weighting for the likelihood of application.
        """
        self.in_type = in_type
        self.out_type = out_type
        self.weight = weight


# Defines the global list of templates to be used within the search algorithm
templates = []

templates.append(AlterTemplate(ast.operator, ast.operator, 1))
templates.append(AlterTemplate(ast.cmpop, ast.cmpop, 1))
templates.append(AlterTemplate(ast.stmt, None, 1))


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
            if isinstance(node, template.in_type):
                if template.out_type is not None:
                    sub_classes = template.out_type.__subclasses__()

                    # Check if the new node is general
                    if len(sub_classes) > 0:
                        for sub_class in sub_classes:
                            candidates[AlterEdit(node.unique_id, sub_class)] = template.weight
                    else:
                        candidates[AlterEdit(node.unique_id, template.out_type)] = template.weight
                else:
                    candidates[AlterEdit(node.unique_id, None)] = template.weight

    return candidates
