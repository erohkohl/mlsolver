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

    def derive(self, world_name):
        return world_name, self, []

    def __eq__(self, other):
        return isinstance(other, Atom) and other.name == self.name

    def __str__(self):
        return "Atom(" + self.name + ")"


class Box:
    """
    Describes box operator of modal logic formula and it's semantics
    """

    def __init__(self, mlp):
        self.mlp = mlp

    def semantic(self, ks, world_to_test):
        result = True
        for relation in ks.relations:
            if relation[0] == world_to_test:
                result = result and self.mlp.semantic(ks, relation[1])
        return result

    # TODO
    def __eq__(self, other):
        raise NotImplementedError

    # TODO
    def __str__(self):
        raise NotImplementedError


class Box_a:
    """
    Describes box operator of modal logic formula and it's semantics for Agent a
    """

    def __init__(self, agent, mlp):
        self.mlp = mlp
        self.agent = agent

    def semantic(self, ks, world_to_test):
        result = True
        for relation in ks.relations.get(self.agent, {}):
            if relation[0] == world_to_test:
                result = result and self.mlp.semantic(ks, relation[1])
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

    def __init__(self, mlp):
        self.mlp = mlp

    def semantic(self, ks, world_to_test, depth=1):
        f = self.mlp
        for agents in ks.relations:
            f = And(f, Box_a(agents, self.mlp))
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

    def __init__(self, mlp):
        self.mlp = mlp

    def semantic(self, ks, world_to_test):
        result = False
        for relation in ks.relations:
            if relation[0] == world_to_test:
                result = result or self.mlp.semantic(ks, relation[1])
        return result

    # TODO
    def __eq__(self, other):
        raise NotImplementedError

    # TODO
    def __str__(self):
        raise NotImplementedError


class Diamond_a:
    """
    Describes diamond operator of modal logic formula and it's semantics for Agent a
    """

    def __init__(self, agent, mlp):
        self.mlp = mlp
        self.agent = agent

    def semantic(self, ks, world_to_test):
        result = False
        for relation in ks.relations.get(self.agent, {}):
            if relation[0] == world_to_test:
                result = result or self.mlp.semantic(ks, relation[1])
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

    def __init__(self, left_mlp, right_mlp):
        self.left_mlp = left_mlp
        self.right_mlp = right_mlp

    def semantic(self, ks, world_to_test):
        return not self.left_mlp.semantic(ks, world_to_test) or self.right_mlp.semantic(ks, world_to_test)

    # TODO
    def __eq__(self, other):
        raise NotImplementedError

    # TODO
    def __str__(self):
        raise NotImplementedError


class Not:
    """
    Describes negation derived from classic propositional logic
    """

    def __init__(self, mlp):
        self.mlp = mlp

    def semantic(self, ks, world_to_test):
        return not self.mlp.semantic(ks, world_to_test)

    # TODO
    def __eq__(self, other):
        raise NotImplementedError

    # TODO
    def __str__(self):
        raise NotImplementedError


class And:
    """
    Describes and derived from classic propositional logic
    """

    def __init__(self, left_mlp, right_mlp):
        self.left_mlp = left_mlp
        self.right_mlp = right_mlp

    def semantic(self, ks, world_to_test):
        return self.left_mlp.semantic(ks, world_to_test) and self.right_mlp.semantic(ks, world_to_test)

    def derive(self, world_name):
        return world_name, self.left_mlp, [(world_name, self.right_mlp)]

    def __eq__(self, other):
        return self.left_mlp == other.left_mlp and self.right_mlp == other.right_mlp

    def __str__(self):
        return "And(" + self.left_mlp.__str__() + ", " + self.right_mlp.__str__() + ")"


class Or:
    """
    Describes or derived from classic propositional logic
    """

    def __init__(self, left_mlp, right_mlp):
        self.left_mlp = left_mlp
        self.right_mlp = right_mlp

    def semantic(self, ks, world_to_test):
        return self.left_mlp.semantic(ks, world_to_test) or self.right_mlp.semantic(ks, world_to_test)

    # TODO
    def __eq__(self, other):
        raise NotImplementedError

    # TODO
    def __str__(self):
        raise NotImplementedError
