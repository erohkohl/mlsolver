# This class describes a Kripke Frame with it's possible worlds and their transition relation. Furthermore it extends
# the graph to Kripke Structure by assigning a subset of propositional variables to each world.
class KripkeStructure:
    def __init__(self, worlds, relations, assignments):
        self.worlds = worlds
        self.relations = relations
        self.assignments = assignments