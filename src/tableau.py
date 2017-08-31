"""Modal logic tableau calculus module

This module contains data structures to store the proof tree of modal logic's
tableau calculus.
"""
from src.formula import *


# Todo delete class ProofTree and make its methods top level of this module?!
class ProofTree:
    """
    Todo
    """

    def __init__(self, formula):
        self.root_node = create_node('s', formula, [])

    def derive(self):
        """Returns a valid Kripke structures if formula is satisfiable.
        """
        next_node = self.root_node.__next__()

        while not next_node is None:
            node_to_add = self.expand_node(next_node)
            leaf = self.root_node.get_leaf()  # Todo add multiple leaf support
            leaf.add_child(node_to_add)
            next_node.is_derived = True
            next_node = self.root_node.__next__()

    def expand_node(self, node):
        if isinstance(node.formula, Atom):
            return None
        if isinstance(node.formula, Not):
            return create_node('s', node.formula.not_mlp, [])
        if isinstance(node.formula, And):
            inner_node = create_node('s', node.formula.right_mlp, [])
            return create_node('s', node.formula.left_mlp, [inner_node])
        if isinstance(node.formula, Or):
            first_node = create_node('s', node.formula.left_mlp, [])
            second_node = create_node('s', node.formula.right_mlp, [])
            return [first_node, second_node]
        return None


def create_node(world_name, formula, children):
    """Routine decides whether a node must be a leaf node, when it is not
    derivable further, or a classical node.
    """
    if isinstance(formula, Atom):
        return Leaf(world_name, formula.name, children, True)
    elif isinstance(formula, Not) and isinstance(formula.not_mlp, Atom):
        return Leaf(world_name, formula.not_mlp.name, children, False)
    else:
        return Node(world_name, formula, children)
    return None


class Node:
    """
    Class represents one node of the proof tree. Therefore it holds one
    world name, its children and a modal logic formula. The property is_
    derived is true, when this node was processed by the solver.
    """

    def __init__(self, world_name, formula, children):
        self.world_name = world_name
        self.children = children
        self.formula = formula
        self.is_derived = False

    def add_child(self, node):
        """Routine adds one child node or list of children to the current
         instance.
        """
        if isinstance(node, list):
            for n in node:
                self.children.append(n)
        elif not node is None:
            self.children.append(node)

    def get_leaf(self):
        """Returns list of nodes, which each node has no children.
        """
        if self.children == []:
            return self
        else:
            for child in self.children:
                return child.get_leaf()

    def __iter__(self):
        return self

    def __next__(self):
        """Return next node, that is not derived yet in post order sequence
        """
        if self.is_derived is False:
            return self
        else:
            for child in self.children:
                if not child.is_derived:
                    return child
                else:
                    return child.__next__()
        return None

    def __eq__(self, other):
        are_children_eq = True
        if other is None:
            return False

        if not len(self.children) == len(other.children):
            return False

        for (self_child, other_child) in zip(self.children, other.children):
            are_children_eq = are_children_eq and self_child == other_child

        return self.world_name == other.world_name \
               and self.is_derived == other.is_derived \
               and self.formula == other.formula \
               and are_children_eq


class Leaf(Node):
    """
    This class does not map a leaf of a tree in sense, that it has no children.
    Moreover this leaf is completely derived, thus it stores only propositional
    variables or their negations.
    """

    def __init__(self, world_name, variable_name, children, assignment):
        super().__init__(world_name, None, children)
        self.variable_name = variable_name
        self.assignment = assignment
        self.is_derived = True

    def __eq__(self, other):
        return self.is_derived \
               and other.is_derived \
               and self.assignment == other.assignment \
               and self.variable_name == other.variable_name \
               and super().__eq__(other)
