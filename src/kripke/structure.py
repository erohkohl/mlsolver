# This class describes a Kripke Frame with it's possible worlds and their transition relation. Furthermore it extends
# the graph to Kripke Structure by assigning a subset of propositional variables to each world.
class KripkeStructure:
    def __init__(self, worlds, relations):
        if isinstance(worlds, list) and isinstance(worlds[0], World):
            self.worlds = worlds
            self.relations = relations
        else:
            raise TypeError


class World:
    def __init__(self, name, assignment):
        self.name = name
        self.assignment = assignment