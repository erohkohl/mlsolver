import networkx as nx
import matplotlib.pyplot as plt

from src.model import WiseMenWithHat


# Routine to plot Kripke Frame with relations for all agents
def draw_graph(ks, labels):
    nodes = set(world.name for world in ks.worlds)
    G = nx.Graph()

    for node in nodes:
        G.add_node(node)

    label = {}
    for agent, l in zip(ks.relations, labels):
        edges = ks.relations.get(agent)
        for edge in edges:
            G.add_edge(edge[0], edge[1])
            label.update({edge: l})

    pos = nx.shell_layout(G)
    nx.draw(G, pos)
    nx.draw_networkx_nodes(G, pos, node_size=3000, node_color="white", linewidths=3.0)

    # labels
    nx.draw_networkx_labels(G, pos, font_size=15, font_family='sans-serif', label_pos=0.1)
    nx.draw_networkx_edge_labels(G, pos, label)


ks = WiseMenWithHat().ks
plt.savefig("./scripts/wise_men_with_hat_graph.png")
draw_graph(ks, ["Wise man 1", "Wise man 2", " Wise man 3"])
plt.show()
