""" Modal logic tableau calculus module

This module contains data structures to store the proof tree of modal logic's tableau calculus .
"""
from src.kripke import *


class ProofTree:
    """
    TODO
    """

    def __init__(self, formula):
        self.root_node = Node('s', formula, [])  # Initial world s, False = not derived yet
        self.ks = KripkeStructure([], {})

    def derive(self):
        """Returns a valid Kripke structures if formula is satisfiable.
        """
        derived_node = self.root_node.formula.derive('s')
        try:  # Pythonic
            self.ks.worlds.append(World(self.root_node.world_name, {self.root_node.formula.name: True}))
        except:
            pass
        try:
            self.ks.worlds.append(World(self.root_node.world_name,
                                        {self.root_node.formula.left_mlp.name: True,
                                         self.root_node.formula.right_mlp.name: True}))
            self.root_node.children.append(derived_node)
        except:
            pass
        return self.ks


class Node:
    """
    TODO
    """

    def __init__(self, world_name, formula, children=[]):
        self.world_name = world_name
        self.formula = formula
        self.is_derived = False
        self.children = children

    def __eq__(self, other):
        are_children_eq = True

        if not len(self.children) == len(other.children):
            return False

        for (self_child, other_child) in zip(self.children, other.children):
            are_children_eq = are_children_eq and self_child == other_child

        return self.world_name == other.world_name \
               and self.formula == other.formula \
               and self.is_derived == other.is_derived \
               and are_children_eq

    def __str__(self):
        children = "["
        for child in self.children:
            children = children + child.__str__() + ', '
        children = children + ']'
        return "Node(" + str(self.world_name) + ', ' + str(self.formula) + ', ' + children + ')'


class Bottom(Node):
    """
    TODO
    """

    def __init__(self):
        self.world_name = None
        self.formula = None
        self.is_derived = True
        self.children = None
