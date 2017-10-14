"""Modal logic formula module

This module unites all operators from propositional and modal logic.
"""


class Atom:
    """
    This class represents propositional logic variables in modal logic formulas.
    """

    def __init__(self, name):
        self.name = name

    def semantic(self, ks, world_to_test):
        """Function returns assignment of variable in Kripke's world.
        """
        for world in ks.worlds:
            if world.name == world_to_test:
                return world.assignment.get(self.name, False)

    def __eq__(self, other):
        return isinstance(other, Atom) and other.name == self.name

    def __str__(self):
        return str(self.name)


class Box:
    """
    Describes box operator of modal logic formula and it's semantics
    """

    def __init__(self, inner):
        self.inner = inner

    def semantic(self, ks, world_to_test):
        result = True
        for relation in ks.relations:
            if relation[0] == world_to_test:
                result = result and self.inner.semantic(ks, relation[1])
        return result

    def __eq__(self, other):
        return isinstance(other, Box) and self.inner == other.inner

    def __str__(self):
        if isinstance(self.inner, Atom):
            return u"\u2610" + " " + str(self.inner)
        else:
            return u"\u2610" + "(" + str(self.inner) + ")"


class Box_a:
    """
    Describes box operator of modal logic formula and it's semantics for Agent a
    """

    def __init__(self, agent, inner):
        self.inner = inner
        self.agent = agent

    def semantic(self, ks, world_to_test):
        result = True
        for relation in ks.relations.get(self.agent, {}):
            if relation[0] == world_to_test:
                result = result and self.inner.semantic(ks, relation[1])
        return result

    # TODO
    def __eq__(self, other):
        raise NotImplementedError

    # TODO
    def __str__(self):
        raise NotImplementedError


class Box_star:
    """
    Describes semantic of multi modal Box^* operator.
    Semantic(Box_star phi) = min(Box Box ... Box phi, for all n in /N)
    Simplification with n = 1: Box_star phi = phi and Box_a phi and Box_b phi ... and Box_n phi
    """

    def __init__(self, inner):
        self.inner = inner

    def semantic(self, ks, world_to_test, depth=1):
        f = self.inner
        for agents in ks.relations:
            f = And(f, Box_a(agents, self.inner))
        return f.semantic(ks, world_to_test)

    # TODO
    def __eq__(self, other):
        raise NotImplementedError

    # TODO
    def __str__(self):
        raise NotImplementedError


class Diamond:
    """
    Describes diamond operator of modal logic formula and it's semantics
    """

    def __init__(self, inner):
        self.inner = inner

    def semantic(self, ks, world_to_test):
        result = False
        for relation in ks.relations:
            if relation[0] == world_to_test:
                result = result or self.inner.semantic(ks, relation[1])
        return result

    def __eq__(self, other):
        return isinstance(other, Diamond) and self.inner == other.inner

    def __str__(self):
        if isinstance(self.inner, Atom):
            return u"\u25C7" + " " + str(self.inner)
        else:
            return u"\u25C7" + "(" + str(self.inner) + ")"


class Diamond_a:
    """
    Describes diamond operator of modal logic formula and it's semantics for Agent a
    """

    def __init__(self, agent, inner):
        self.inner = inner
        self.agent = agent

    def semantic(self, ks, world_to_test):
        result = False
        for relation in ks.relations.get(self.agent, {}):
            if relation[0] == world_to_test:
                result = result or self.inner.semantic(ks, relation[1])
        return result

    # TODO
    def __eq__(self, other):
        raise NotImplementedError

    # TODO
    def __str__(self):
        raise NotImplementedError


class Implies:
    """
    Describes implication derived from classic propositional logic
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def semantic(self, ks, world_to_test):
        return not self.left.semantic(ks, world_to_test) or self.right.semantic(ks, world_to_test)

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __str__(self):
        return "(" + self.left.__str__() + " -> " + self.right.__str__() + ")"


class Not:
    """
    Describes negation derived from classic propositional logic
    """

    def __init__(self, inner):
        self.inner = inner

    def semantic(self, ks, world_to_test):
        return not self.inner.semantic(ks, world_to_test)

    def __eq__(self, other):
        return self.inner == other.inner

    def __str__(self):
        return u"\uFFE2" + str(self.inner)


class And:
    """
    Describes and derived from classic propositional logic
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def semantic(self, ks, world_to_test):
        return self.left.semantic(ks, world_to_test) and self.right.semantic(ks, world_to_test)

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __str__(self):
        return "(" + self.left.__str__() + " " + u"\u2227" + " " + self.right.__str__() + ")"


class Or:
    """
    Describes or derived from classic propositional logic
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def semantic(self, ks, world_to_test):
        return self.left.semantic(ks, world_to_test) or self.right.semantic(ks, world_to_test)

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __str__(self):
        return "(" + self.left.__str__() + " " + u"\u2228" + " " + self.right.__str__() + ")"
