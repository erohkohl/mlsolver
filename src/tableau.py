""" Modal logic tableau calculus module

This module contains data structures to store the proof tree of modal logic's tableau calculus .
"""
from src.kripke import *
from src.formula import Atom, And, Not


class ProofTree:
    """
    TODO
    """

    def __init__(self, formula):
        self.root_node = Node('s', formula)  # Initial world s, False = not derived yet
        self.ks = KripkeStructure([], {})

    def derive(self):
        """Returns a valid Kripke structures if formula is satisfiable.
        """
        world_name, formula, children = self.root_node.formula.derive('s')
        self.root_node.children.append(Node(world_name, formula, children))

        if isinstance(self.root_node.formula, Atom):  # TODO not Pythonic -> try
            self.ks.worlds.append(World(self.root_node.world_name, {self.root_node.formula.name: True}))
        if isinstance(self.root_node.formula, And):  # TODO not Pythonic
            self.ks.worlds.append(
                World(self.root_node.world_name,
                      {self.root_node.formula.left_mlp.name: True, self.root_node.formula.right_mlp.name: True}))
        if isinstance(self.root_node.formula, Not):
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
        return self.world_name == other.world_name \
               and self.formula == other.formula \
               and self.is_derived == other.is_derived \
               and self.children == self.children


class Bottom(Node):
    """
    TODO
    """

    def __init__(self):
        self.world_name = None
        self.formula = None
        self.is_derived = True
        self.children = None
