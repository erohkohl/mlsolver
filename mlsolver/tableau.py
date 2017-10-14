"""Modal logic tableau module

This module contains data structures, that describe the proof tree of
modal logic formula and the rules of the tableau calculus.
"""
from mlsolver.formula import *
from mlsolver.kripke import *


class ProofTree:
    """
    The ProofTree determines one node instance as root of the tableau.
    This root node maps the modal logic formula, that should be solved.
    Moreover this class holds a valid Kripke structure, if the formula
    is satisfiable. Therefore the routine derive() manages the control
    flow, that checks if the tree has not derived nodes, expands these
    nodes, adds their children to the leafs and checks whether a path
    is closed.
    """

    def __init__(self, formula):
        self.WORLDS = ['t', 's']
        self.start_world = self.WORLDS.pop()
        self.root_node = self.create_node(self.start_world, formula, [])
        self.root_node.partial_assign = {self.start_world: {}}
        self.kripke_structure = None
        self.is_closed = None

    def derive(self):
        """Determines a valid Kripke structure if formula is satisfiable.
        """
        next_node = self.root_node.__next__()

        while next_node is not None:
            leafs = next_node.get_all_leafs()
            for leaf in leafs:
                leaf.add_child(self.expand_node(next_node))
            next_node.is_derived = True
            next_node = self.root_node.__next__()
        check_conflict(self.root_node)

        """
        Find leaf, that has no children and return its partial assignment
        and relations as Kripke structure. The property solutions_leaf stores 
        all leafs of the fully derived proof tree, to check whether formula is 
        satisfiable.
        """
        solutions_leafs = self.root_node.get_all_leafs()
        if solutions_leafs == []:
            pass
        else:
            for leaf in solutions_leafs:
                if not isinstance(leaf, Bottom):
                    worlds = []
                    for world_name, assign in leaf.partial_assign.items():
                        world = World(world_name, assign)
                        worlds.append(world)

                    self.kripke_structure = KripkeStructure(worlds, leaf.relations)
                    return
            self.is_closed = True

    def create_node(self, world_name, formula, children):
        """Routine decides whether a node must be a leaf node, when it is not
        derivable further, or a classical node.
        """
        if isinstance(formula, Atom):
            return Leaf(world_name, formula.name, children, True)
        elif isinstance(formula, Not) and isinstance(formula.inner, Atom):
            return Leaf(world_name, formula.inner.name, children, False)
        else:
            return Node(world_name, formula, children)
        return None

    def resolve_box_operator(self, node, new_world):
        """Walks through all parent nodes and check whether box operator
        forces formula in new world
        """
        leafs = []
        if node.parent is None:
            return leafs
        if isinstance(node.formula, Box):
            leaf = self.create_node(new_world, node.formula.inner, [])
            leaf.relations.add((node.world, new_world))
            leafs.append(leaf)
        return leafs + self.resolve_box_operator(node.parent, new_world)

    def expand_node(self, node):
        """Contains all rules of tableau calculus and tries to match them to a node
        """
        if isinstance(node.formula, Atom):
            return None

        if isinstance(node.formula, Not):
            formula = node.formula.inner
            if isinstance(formula, Not):
                return self.create_node(node.world, formula.inner, [])
            if isinstance(formula, Or):
                inner_node = self.create_node(node.world, Not(formula.right), [])
                return self.create_node(node.world, Not(formula.left), [inner_node])
            if isinstance(formula, And):
                first_node = self.create_node(node.world, Not(formula.left), [])
                second_node = self.create_node(node.world, Not(formula.right), [])
                return [first_node, second_node]
            if isinstance(formula, Implies):
                inner_node = self.create_node(node.world, Not(formula.right), [])
                return self.create_node(node.world, formula.left, [inner_node])
            if isinstance(formula, Box):
                return self.create_node(node.world, Diamond(Not(formula.inner)), [])
            if isinstance(formula, Diamond):
                return self.create_node(node.world, Box(Not(formula.inner)), [])
            return self.create_node(node.world, formula, [])

        if isinstance(node.formula, And):
            inner_node = self.create_node(node.world, node.formula.right, [])
            outer_node = self.create_node(node.world, node.formula.left, [inner_node])
            inner_node.parent = outer_node
            return outer_node

        if isinstance(node.formula, Or):
            first_node = self.create_node(node.world, node.formula.left, [])
            second_node = self.create_node(node.world, node.formula.right, [])
            return [first_node, second_node]

        if isinstance(node.formula, Implies):
            first_node = self.create_node(node.world, Not(node.formula.left), [])
            second_node = self.create_node(node.world, node.formula.right, [])
            return [first_node, second_node]

        if isinstance(node.formula, Diamond):
            next_world = self.WORLDS.pop()
            leafs_forced_by_box = self.resolve_box_operator(node, next_world)
            node_to_add = self.create_node(next_world, node.formula.inner, leafs_forced_by_box)
            node_to_add.relations.add((node.world, next_world))
            return node_to_add

        return None

    def __str__(self):
        return "Proof tree\n==========\n" + str(self.root_node) + \
               '\n' + "Kripke structure\n================\n" + str(self.kripke_structure)


def check_conflict(node):
    """Routine walks through each node and checks whether leafs force
    conflict with partial assignment.
    """

    if isinstance(node, Leaf):
        try:
            if not node.partial_assign[node.world][node.variable_name] is node.assign:
                node.children = Bottom()
                return
        except:
            try:
                node.partial_assign[node.world].update({node.variable_name: node.assign})
            except:
                node.partial_assign[node.world] = {node.variable_name: node.assign}
    for child in node.children:
        child.partial_assign.update(copy.deepcopy(node.partial_assign))
        check_conflict(child)


class Node:
    """
    Class represents one node of the proof tree. Therefore it holds one
    world name, its children and a modal logic formula. Its property is_
    derived is true, when this node was processed by the solver.
    """

    def __init__(self, world, formula, children):
        self.world = world
        self.children = children
        self.formula = formula
        self.is_derived = False
        self.partial_assign = dict()
        self.relations = set()
        self.parent = None
        self.level = 0

    def add_child(self, nodes):
        """Routine adds one child node or list of children to the current
        node instance.
        """
        if isinstance(nodes, list):
            for node in nodes:
                self.children.append(node)
                node.parent = self
                node.relations.update(self.relations)
        elif not nodes is None:
            # Just one node to add, not list
            self.children.append(nodes)
            nodes.parent = self
            nodes.relations.update(self.relations)

    def get_all_leafs(self):
        """Returns a list of nodes, where each node has no children.
        """
        leafs = []

        if self.children == []:
            leafs.append(self)
        elif not isinstance(self.children, Bottom):
            for child in self.children:
                for child_leafs in child.get_all_leafs():
                    leafs.append(child_leafs)
        return leafs

    def __iter__(self):
        return self

    def __next__(self):
        """Return next node, that is not derived yet in post order sequence.
        """
        if self.is_derived is False:
            return self
        if isinstance(self.children, Bottom) or isinstance(self, Bottom):
            return None
        else:
            for child in self.children:
                if not child.is_derived:
                    return child
                if child.__next__() is not None:
                    return child.__next__()
        return None

    def __eq__(self, other):
        are_children_eq = True
        if other is None:
            return False

        if isinstance(self.children, Bottom) or isinstance(other.children, Bottom):
            return self.children == other.children
        elif not len(self.children) == len(other.children):
            return False

        for (self_child, other_child) in zip(self.children, other.children):
            are_children_eq = are_children_eq and self_child == other_child

        return self.world == other.world \
               and self.is_derived == other.is_derived \
               and self.formula == other.formula \
               and are_children_eq

    def __str__(self):
        indent = "   "
        if self.level == 0:
            tree_str = repr(self) + "\n"
        else:
            if isinstance(self.children, Bottom):
                end_str = repr(self.children) + "\n"
            else:
                end_str = "\n"
            rel_str = ""
            try:
                # Adds tuple with world names, if path contains diamond
                if not self.world == self.parent.world:
                    rel_str = indent * (self.level - 1) \
                              + ' (' + self.parent.world + ', ' + self.world + ')' \
                              + "\n" + indent * self.level + "| \n"
            except:
                pass
            tree_str = indent * self.level + "| \n" + \
                       rel_str + \
                       indent * self.level + "|_ " + repr(self) + end_str

        if not isinstance(self.children, Bottom):
            for child in self.children:
                child.level = self.level + 1
                tree_str += child.__str__()
        return tree_str

    def __repr__(self):
        return self.world + ':' + str(self.formula)


class Leaf(Node):
    """
    This class does not map a leaf of a tree in sense, that it has no children.
    Moreover is shows, that a node is completely derived, thus it only stores
    propositional variables or their negations.
    """

    def __init__(self, world_name, variable_name, children, assign):
        super().__init__(world_name, None, children)
        self.variable_name = variable_name
        self.assign = assign
        self.is_derived = True

    def __eq__(self, other):
        return super().__eq__(other) \
               and self.is_derived \
               and other.is_derived \
               and self.assign == other.assign \
               and self.variable_name == other.variable_name

    def __str__(self):
        return super(Leaf, self).__str__()

    def __repr__(self):
        if self.assign:
            return self.world + ':' + str(self.variable_name)
        else:
            return self.world + ': ' + u"\uFFE2" + str(self.variable_name)


class Bottom(Node):
    """
    Marks one branch of proof tree as conflict, therefore an instance of this class
    will be assigned to the children of a Leaf node.
    """

    def __init__(self):
        super().__init__(None, None, None)
        self.is_derived = True
        self.children = None

    def __eq__(self, other):
        try:
            return self.is_derived and other.is_derived \
                   and self.children is None and other.children is None
        except:
            return False

    def __iter__(self):
        return self

    def __str__(self):
        return "\t" * self.level + repr(self) + "\n"

    def __repr__(self):
        return ' -|'
