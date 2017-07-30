# This class represents propositional logic variables in modal logic formulas
class Atom():
    def __init__(self, name):
        self.name = name

    def semantic(self, ks, world_to_test):
        for world in ks.worlds:
            if world.name == world_to_test:
                for assign in world.assignment:
                    if assign[0] == self.name:
                        return assign[1]


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