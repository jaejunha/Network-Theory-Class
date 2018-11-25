#!python3
'''
Code for 2018 Network Theory HW#4-3
'''

import networkx as nx
import json
import math
import matplotlib.pyplot as plt

def read_json_file(filename):
    '''
    Reads json file & returns networkx graph instance
    '''
    with open(filename) as f:
        js_graph = json.load(f)
    return nx.readwrite.json_graph.node_link_graph(js_graph)

def draw_graph_with_edgecost(G, list_colors, list_widths):
    '''
    You may be happy by using this...
    Draw networkx graph with edge cost attribute
    '''
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos, edge_color=list_colors, width=list_widths)
    labels = nx.get_edge_attributes(G, "cost")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()


def solve(filename):
    ## Your lines of code
    ## that TA will
    ## use to check correctness

    ## TA's code
    G = read_json_file(filename)

    ## My code

    ## Size
    size_nodes = len(G.nodes())

    ## Nodes
    node_source = list(G.nodes)[0]
    
    ## S
    list_S = set()
    list_S.add(node_source)
    bool_S = {}
    for i in range(size_nodes):
        bool_S[i] = False
    bool_S[node_source] = True

    ## T
    list_T = []

    ## Find C
    C = 0
    for edge in G.edges():
        if G[edge[0]][edge[1]]["cost"] > C:
            C = G[edge[0]][edge[1]]["cost"]

    ## Initialize d and pred
    list_d = {}
    list_pred = {}
    for node in G.nodes():
        if node == node_source:
            list_d[node] = 0
        else:
            list_d[node] = C + 1

    for node in G[node_source]:
        list_d[node] = G[node_source][node]["cost"]
        list_pred[node] = node_source

    ## Cost
    total = 0

    ## Need to add while statement
    while len(list_T) < size_nodes - 1:

        ## Select a node i satisfying d(i) = min{d(j) : node j is not included in S }
        min = C + 1
        node_i = None
        for node in G.nodes():
            if bool_S[node] == True:
                continue
            if min > list_d[node]:
                min = list_d[node]
                node_i = node
        
        ## Update cost
        total += min

        ## Update T
        list_T.append((list_pred[node_i], node_i))

        ## Update S
        list_S.add(node_i)
        bool_S[node_i] = True

        ## Update d
        for node in G[node_i]:
            if G[node_i][node]["cost"] < list_d[node]:
                list_d[node] = G[node_i][node]["cost"]
                list_pred[node] = node_i

    ## Print result
    print('cost is', total)
    print(list_T)

    ## Make new graph
    G_result = nx.Graph()

    ## Copy existing graph nodes
    for node in G.nodes():
        G_result.add_node(node)

    ## Copy existing graph edges
    for edge in G.edges():
        G_result.add_edge(edge[0], edge[1])
        G_result[edge[0]][edge[1]]["cost"] = G[edge[0]][edge[1]]["cost"]
        G_result[edge[0]][edge[1]]["color"] = "black"
        G_result[edge[0]][edge[1]]["width"] = 0.5
    
    ## Copy solution to represent graph
    for edge in list_T:
        G_result[edge[0]][edge[1]]["color"] = "orange"
        G_result[edge[0]][edge[1]]["width"] = 2

    ## Get colors
    list_colors = [G_result[i][j]["color"] for i,j in G_result.edges()]

    ## Get width
    list_widths = [G_result[i][j]["width"] for i,j in G_result.edges()]

    ## Show the graph 
    draw_graph_with_edgecost(G_result, list_colors, list_widths)

    solution = list_T
    return solution

def main():

    filename = "nt_hw4_graph1.json"
    solve(filename)

if __name__ == '__main__':
    main()