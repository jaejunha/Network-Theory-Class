#=========================================================================================
'''
Modules
'''
import json
import queue
import networkx as nx

#=========================================================================================
'''
Variables
'''
##########################################################################################
# size:         number of nodes                                                          #
# distance:     distance variable                                                        #
# capacity:     capacity variable                                                        #
# flow:         flow variable                                                            #
# excess:       excess variable                                                          #
# active_nodes: active nodes variable                                                    #
##########################################################################################

size = 0
distance = {}
capacity = {}
flow = {}
excess = {}
active_nodes = set([])

#=========================================================================================
'''
Read json file and make network object
'''
def read_json_file(filename):
    '''
    graph making from json file
    '''
    with open(filename) as f:
        js_graph = json.load(f)
    return nx.readwrite.json_graph.node_link_graph(js_graph)
   
#=========================================================================================

'''
Initialize distances using BFS method
'''
def init_dist(original_graph):
    
    # To check visited node
    visited_node = {}

    # To use BFS method
    q = queue.Queue()

    # Initialize visited node
    for i in original_graph.nodes:
        visited_node[i] = False

    # Check node 't'
    distance['t'] = 0
    visited_node['t'] = True

    # Find neighbor nodes
    for i,j in original_graph.in_edges('t'):
        q.put((i, 1))

    ##################
    ### BFS method ###
    ##################
    while q.qsize() > 0:
        temp = q.get()
        
        # Already visited
        if visited_node[temp[0]] == True:
            continue

        # Check current node
        distance[temp[0]] = temp[1]
        visited_node[temp[0]] = True

        # Find neighbor nodes
        for i, j in original_graph.in_edges(temp[0]):
            q.put((i, temp[1] + 1))    
  
    # Distance of 's' node
    distance['s'] = size

    # Distance of non visited node
    for i in original_graph:
        if visited_node[i] == False:
            distance[i] = size
   
#=========================================================================================
'''
Initialize information of flow, excess, active nodes
'''
def init_etc(original_graph):
    
    # To make two dimension array
    for i in original_graph.nodes:
        flow[i] = {}
        capacity[i] = {}

    # Initialize variable
    for i in original_graph.nodes:
        excess[i] = 0
        for j in original_graph[i]:
            capacity[i][j] = capacity[j][i] = original_graph[i][j]['capacity']
            flow[i][j] = 0
            flow[j][i] = capacity[i][j]

    # Initialize start node information
    for i in original_graph['s']:
        excess[i] = capacity['s'][i]
        flow['s'][i] = capacity['s'][i]
        flow[i]['s'] = 0
        active_nodes.add(i)

#=========================================================================================
'''
Do push action or relabel action
'''
def push_n_relabel(node):

    target = None
    flow_min = size
    is_admissible = False

    ##################
    ### Admissible ###
    ##################
    for i in flow[node]:

        # Check admissible        
        if ((distance[i] + 1) == distance[node]) and (capacity[node][i] > flow[node][i]):
            is_admissible = True

            # Get volume of flow
            if flow_min > capacity[node][i] - flow[node][i]:
                flow_min = capacity[node][i] - flow[node][i]
                target = i

    ############
    ### Push ###
    ############
    if is_admissible == True:

        # Get minimum volume of flow
        flow_min = min(flow_min, excess[node])

        # Update excess
        excess[node] -= flow_min
        excess[target] += flow_min

        # Update flow
        flow[node][target] += flow_min
        flow[target][node] -= flow_min

        # Add active node
        if excess[node] > 0 and distance[node] < size:
            active_nodes.add(node)
        if excess[target] > 0 and target !='t' and distance[target] < size:
            active_nodes.add(target)

    ###############
    ### Relabel ###
    ###############
    else:
        dist_min = size
   
        # Find minimum distance
        for i in flow[node]:
            if capacity[node][i] > flow[node][i]:
                dist_min = min(dist_min, distance[i])

        # Update distance
        distance[node] = 1 + dist_min

        # Add active node
        if excess[node] > 0 and node != 't' and distance[node] < size:
            active_nodes.add(node)
    
#=========================================================================================
'''
Get solution
'''
def solve(filename):


    ##################
    ### Preprocess ###
    ##################
    # Read json file
    original_graph = read_json_file(filename)

    # Size of nodes
    global size
    size = len(original_graph.nodes)

    # Initialize distance
    init_dist(original_graph)

    # Initialize etc
    init_etc(original_graph)

    #################
    ### Algorithm ###
    #################
    while len(active_nodes) > 0:
        node = active_nodes.pop()
        push_n_relabel(node)

    ##################
    ### Conclusion ###
    ##################
    # Get maximum flow
    flow_value = 0
    for i, j in original_graph.in_edges('t'):
        flow_value += flow[i][j]
   
    # Get flow information
    flow_dict = {}
    for i in original_graph.nodes:
        flow_dict[i] = {}
        for j in original_graph[i]:
            flow_dict[i][j] = flow[i][j]

    return flow_value, flow_dict

#=========================================================================================
'''
Main function
'''
def main():
    filename = "nt_hw5_graph3.json"
    value, dictionary = solve(filename)
    print("Maxflow value:", value)
    print("Dictionary of flow:")
    import pprint
    pprint.pprint(dictionary)

#=========================================================================================
'''
Start program
'''
if __name__ == '__main__':
    main()