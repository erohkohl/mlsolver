# This class describes a Kripke Frame with it's possible worlds and their transition relation.
class KripkeStructure:
    def __init__(self, worlds, relations):
        if not isinstance(worlds, list) or isinstance(worlds[0], World):
            self.worlds = worlds
            self.relations = relations
        else:
            raise TypeError

    # Removes one node of Kripke frame, therefore we can make knowledge base consistent with announcement.
    def remove_node(self, node_name):
        worlds = self.worlds.copy()
        for world in worlds:
            if node_name == world.name:
                self.worlds.remove(world)
                relations = self.relations.copy()
                for (i, j) in relations:
                    if i == node_name or j == node_name:
                        self.relations.remove((i, j))
                return
        raise ValueError

    def __eq__(self, other):
        for (i, j) in zip(self.worlds, other.worlds):
            if not i.__eq__(j):
                return False
        for (i, j) in zip(self.relations, other.relations):
            if not i == j:
                return False
        return True


# Represents the nodes of Kripke and it extends the graph to Kripke Structure by assigning a subset of propositional
# variables to each world.
class World:
    def __init__(self, name, assignment):
        self.name = name
        self.assignment = assignment

    def __eq__(self, other):
        return self.name == other.name and self.assignment == other.assignment
