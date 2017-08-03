import networkx as nx
import matplotlib.pyplot as plt

from src.model import WiseMenWithHat
import src.model as Model


# Routine to plot Kripke Frame with relations for all agents
def draw_graph(ks, labels, nodes_not_follow_formula):
    nodes = list(world.name for world in ks.worlds)
    G = nx.Graph()

    for node in nodes:
        G.add_node(node)

    label = {}
    edge_list = []
    for agent, l in zip(ks.relations, labels):
        edges = ks.relations.get(agent)
        for edge in edges:
            edge_list.append((edge[0], edge[1]))
            label.update({edge: l})

    pos = nx.shell_layout(G)
    nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_size=3000, node_color="green", linewidths=3.0)
    nx.draw_networkx_nodes(G, pos, nodelist=nodes_not_follow_formula, node_size=3000, node_color="red",
                           linewidths=3.0)
    nx.draw_networkx_edges(G, pos, edgelist=edge_list, width=2, alpha=0.5, edge_color='black')

    # labels
    nx.draw_networkx_labels(G, pos, font_size=15, font_family='sans-serif', label_pos=0.1)
    nx.draw_networkx_edge_labels(G, pos, label)

    plt.axis('off')


wise_men_model = WiseMenWithHat()
ks = wise_men_model.ks

draw_graph(ks, ["1", "2", "3"],
           Model.nodes_not_follow_formula(wise_men_model.implicit_knowledge_one, wise_men_model.ks))
draw_graph(ks, ["1", "2", "3"],
           Model.nodes_not_follow_formula(wise_men_model.announcement_three, wise_men_model.ks))

plt.show()