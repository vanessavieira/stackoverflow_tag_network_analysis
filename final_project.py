import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import community
import scipy


def read_data():
    nodes = pd.read_csv('stack_network_nodes.csv')
    edges = pd.read_csv('stack_network_links.csv')
    return nodes, edges


def define_network(nodes, edges):
    # creating networkx network from data
    G = nx.Graph()
    for index, row in nodes.iterrows():
        G.add_node(row["name"], group=row["group"], nodesize=row["nodesize"])

    for index, row in edges.iterrows():
        G.add_edge(row["source"], row["target"], weight=row["value"])

    return G


def plot_network(G, pos, size):
    # nodes = G.nodes()
    # color_map = {1: '#f09494', 2: '#eebcbc', 3: '#72bbd0', 4: '#91f0a1', 5: '#629fff', 6: '#bcc2f2',
    #              7: '#eebcbc', 8: '#f1f0c0', 9: '#d2ffe7', 10: '#caf3a6', 11: '#ffdf55', 12: '#ef77aa',
    #              13: '#d6dcff', 14: '#d2f5f0'}
    # node_color = [color_map[d['group']] for n, d in G.nodes(data=True)]
    # node_size = [d['nodesize'] * 10 for n, d in G.nodes(data=True)]
    plt.figure(figsize=size)
    # node_color=node_color, node_size=node_size
    nx.draw_networkx(G, pos=pos, node_color='lightcoral',edge_color='#FFDEA2', edge_width=1)
    plt.show()


def plot_community_detection(G, pos):

    plt.figure(figsize=(25, 25))
    partition = community.best_partition(G)
    size = float(len(set(partition.values())))
    # print("size = " + str(size))
    count = 0
    colors = ['#f09494','#eebcbc', '#72bbd0', '#91f0a1', '#629fff', '#bcc2f2',
              '#eebcbc', '#f1f0c0', '#d2ffe7', '#caf3a6', '#ffdf55', '#ef77aa','#d6dcff','#d2f5f0']
    for com in set(partition.values()):
        list_nodes = [nodes for nodes in partition.keys()
                      if partition[nodes] == com]

        edges_sizes = []
        list_nodes_G = G.nodes._nodes

        for n in list_nodes:
            edges_sizes.append(list_nodes_G[str(n)]['nodesize'] * 10)

        nx.draw_networkx_nodes(G, pos, list_nodes, node_size=edges_sizes,
                               node_color=colors[count])
        nx.draw_networkx_labels(G, pos, {n: n for n in list_nodes}, font_size=10)
        count = count + 1

    nx.draw_networkx_edges(G, pos, alpha=0.5, edge_color='#FFDEA2', edge_width=1)

    plt.show()


def main():

    nodes, edges = read_data()

    G = define_network(nodes, edges)

    pos = nx.drawing.spring_layout(G, k=0.70, iterations=60)

    plot_network(G, pos, size=(25, 25))

    plot_community_detection(G, pos)


if __name__ == "__main__":
    main()