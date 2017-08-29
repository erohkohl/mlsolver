""" Modal logic tableau calculus module

This module contains data structures to store the proof tree of modal logic's tableau calculus .
"""
from src.kripke import *
from src.formula import *


class ProofTree:
    """
    TODO
    """

    def __init__(self, formula):
        self.root_node = Node('s', formula, [])


    def derive(self):
        """Returns a valid Kripke structures if formula is satisfiable.
        """
        next_node = self.root_node.__next__()
        node_to_add = self.expand_node(next_node)
        next_node.add_child(node_to_add)
        next_node.is_derived = True

        next_node = self.root_node.__next__()
        node_to_add = self.expand_node(next_node)
        next_node.add_child(node_to_add)
        next_node.is_derived = True

        next_node = self.root_node.__next__()
        node_to_add = self.expand_node(next_node)
        next_node.add_child(node_to_add)
        next_node.is_derived = True



    def expand_node(self, node):
        if isinstance(node.formula, Atom):
            return None
        if isinstance(node.formula, And):
            node_to_add = Node('s', node.formula.left_mlp, [Node('s', node.formula.right_mlp, [])])
        return node_to_add


class Node():
    def __init__(self, world_name, formula, children):
        self.world_name = world_name
        self.formula = formula
        self.children = children
        self.is_derived = False

    def add_child(self, node):
        """TODO
        """
        if not node == None:
            self.children.append(node)

    def __iter__(self):
        return self

    def __next__(self):
        """Return next node, that is not derived yet in post order sequence
        """
        if self.is_derived == False:
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
        if other == None:
            return False

        if not len(self.children) == len(other.children):
            return False

        for (self_child, other_child) in zip(self.children, other.children):
            are_children_eq = are_children_eq and self_child == other_child

        return self.world_name == other.world_name \
               and self.is_derived == other.is_derived \
               and self.formula == other.formula \
               and are_children_eq
