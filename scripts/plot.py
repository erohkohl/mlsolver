import networkx as nx
import matplotlib.pyplot as plt

from src.model import WiseMenWithHat
import src.model as Model


# Routine to plot Kripke Frame with relations for all agents
def draw_graph(ks, labels, nodes_one, color_one, nodes_two, color_two):
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
    nx.draw_networkx_nodes(G, pos, nodelist=nodes_one, node_size=3000, node_color=color_one,
                           linewidths=3.0)
    nx.draw_networkx_nodes(G, pos, nodelist=nodes_two, node_size=3000, node_color=color_two,
                           linewidths=3.0)
    nx.draw_networkx_edges(G, pos, edgelist=edge_list, width=2, alpha=0.5, edge_color='black')

    # labels
    nx.draw_networkx_labels(G, pos, font_size=15, font_family='sans-serif', label_pos=0.1)
    nx.draw_networkx_edge_labels(G, pos, label)

    plt.axis('off')


wise_men_model = WiseMenWithHat()
ks = wise_men_model.ks

#nodes = Model.nodes_not_follow_formula(wise_men_model.implicit_knowledge_one, wise_men_model.ks)
#nodes_two = Model.nodes_not_follow_formula(wise_men_model.announcement_three, wise_men_model.ks)
#for x in nodes:
 #   nodes_two.remove(x)

#draw_graph(ks, ["1", "2", "3"], nodes, "orange", nodes_two, "red")
#f = plt.figure(1)
#f.set_facecolor('w')
#plt.show()
