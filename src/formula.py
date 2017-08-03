# This class represents propositional logic variables in modal logic formulas
class Atom():
    def __init__(self, name):
        self.name = name

    def semantic(self, ks, world_to_test):
        for world in ks.worlds:
            if world.name == world_to_test:
                return world.assignment.get(self.name, False)


# Describes box operator of modal logic formula and it's semantics
class Box():
    def __init__(self, mlp):
        self.mlp = mlp

    def semantic(self, ks, world_to_test):
        result = True
        for relation in ks.relations:
            if relation[0] == world_to_test:
                result = result and self.mlp.semantic(ks, relation[1])

        return result


# Describes box operator of modal logic formula and it's semantics for Agent a
class Box_a():
    def __init__(self, agent, mlp):
        self.mlp = mlp
        self.agent = agent

    def semantic(self, ks, world_to_test):
        result = True
        for relation in ks.relations.get(self.agent, {}):
            if relation[0] == world_to_test:
                result = result and self.mlp.semantic(ks, relation[1])

        return result


# Describes diamond operator of modal logic formula and it's semantics
class Diamond():
    def __init__(self, mlp):
        self.mlp = mlp

    def semantic(self, ks, world_to_test):
        result = False
        for relation in ks.relations:
            if relation[0] == world_to_test:
                result = result or self.mlp.semantic(ks, relation[1])

        return result


# Describes diamond operator of modal logic formula and it's semantics for Agent a
class Diamond_a():
    def __init__(self, agent, mlp):
        self.mlp = mlp
        self.agent = agent

    def semantic(self, ks, world_to_test):
        result = False
        for relation in ks.relations.get(self.agent, {}):
            if relation[0] == world_to_test:
                result = result or self.mlp.semantic(ks, relation[1])

        return result


# Describes implication derived from classic propositional logic
class Implies():
    def __init__(self, left_mlp, right_mlp):
        self.left_mlp = left_mlp
        self.right_mlp = right_mlp

    def semantic(self, ks, world_to_test):
        return not self.left_mlp.semantic(ks, world_to_test) or self.right_mlp.semantic(ks, world_to_test)


# Describes negation derived from classic propositional logic
class Not():
    def __init__(self, mlp):
        self.mlp = mlp

    def semantic(self, ks, world_to_test):
        return not self.mlp.semantic(ks, world_to_test)


# Describes and derived from classic propositional logic
class And():
    def __init__(self, left_mlp, right_mlp):
        self.left_mlp = left_mlp
        self.right_mlp = right_mlp

    def semantic(self, ks, world_to_test):
        return self.left_mlp.semantic(ks, world_to_test) and self.right_mlp.semantic(ks, world_to_test)


# Describes or derived from classic propositional logic
class Or():
    def __init__(self, left_mlp, right_mlp):
        self.left_mlp = left_mlp
        self.right_mlp = right_mlp

    def semantic(self, ks, world_to_test):
        return self.left_mlp.semantic(ks, world_to_test) or self.right_mlp.semantic(ks, world_to_test)
