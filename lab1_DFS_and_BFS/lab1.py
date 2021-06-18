# MIT 6.034 Lab 1: Search
# Written by 6.034 staff

from search import Edge, UndirectedGraph, do_nothing_fn, make_generic_search
import read_graphs
from functools import reduce

all_graphs = read_graphs.get_graphs()
GRAPH_0 = all_graphs['GRAPH_0']
GRAPH_1 = all_graphs['GRAPH_1']
GRAPH_2 = all_graphs['GRAPH_2']
GRAPH_3 = all_graphs['GRAPH_3']
GRAPH_FOR_HEURISTICS = all_graphs['GRAPH_FOR_HEURISTICS']


## Useful things that I did in this code:
# DFS and BFS in a graph

# Please see wiki lab page for full description of functions and API.

#### PART 1: Helper Functions ##################################################

def path_length(graph, path):
    """Returns the total length (sum of edge weights) of a path defined by a
    list of nodes coercing an edge-linked traversal through a graph.
    (That is, the list of nodes defines a path through the graph.)
    A path with fewer than 2 nodes should have length of 0.
    You can assume that all edges along the path have a valid numeric weight."""
    
    if len(path) <2:
        return 0
    pathlength=0
    for node in range(len(path)-1): #iterates through path but length -1 to avoid going over the list
        edge = graph.get_edge(path[node], path[node+1]) # uses graph method to
        #give us an Edge instance
        #adds the edge length to the path length
        pathlength += edge.length
    return pathlength
    
        
        

def has_loops(path):
    """Returns True if this path has a loop in it, i.e. if it
    visits a node more than once. Returns False otherwise."""
    #create a dictionary to see how many times it occurs in a list
    # if it occurs more than once than return true

    #if there is a loop, it visits a node more than once
    node_dict = {}
    for node in path:
        if node not in node_dict.keys():
            node_dict[node] = 1
        else: 
            node_dict[node] += 1
    for node in node_dict.keys():
        if node_dict[node]>1:
            return True
    return False

def extensions(graph, path):
    """Returns a list of paths. Each path in the list should be a one-node
    extension of the input path, where an extension is defined as a path formed
    by adding a neighbor node (of the final node in the path) to the path.
    Returned paths should not have loops, i.e. should not visit the same node
    twice. The returned paths should be sorted in lexicographic order."""
    path_list = []
    neighbors= graph.get_neighbors(path[-1]) #gets neighboring nodes
    
    for neighbor in neighbors:
        new_path = path.copy()
        
        #extends the list by one neighboring node
        new_path.append(neighbor)
        
        if not has_loops(new_path):#checks to make sure there are no repeat nodes
            path_list.append(new_path)
    return path_list
    
def sort_by_heuristic(graph, goalNode, nodes):
    """Given a list of nodes, sorts them best-to-worst based on the heuristic
    from each node to the goal node. Here, and in general for this lab, we
    consider a smaller heuristic value to be "better" because it represents a
    shorter potential path to the goal. Break ties lexicographically by 
    node name."""
    
    
    nodes.sort() #to get it lexographically and then by heuristic value

    #sorts the nodes by heuristic value
    sorted_nodes = sorted(nodes, key=lambda node: graph.get_heuristic_value(node, goalNode))
    return sorted_nodes

# You can ignore the following line.  It allows generic_search (PART 3) to
# access the extensions and has_loops functions that you just defined in PART 1.
generic_search = make_generic_search(extensions, has_loops)  # DO NOT CHANGE


#### PART 2: Basic Search ######################################################

def basic_dfs(graph, startNode, goalNode):
    """
    Performs a depth-first search on a graph from a specified start
    node to a specified goal node, returning a path-to-goal if it
    exists, otherwise returning None.
    Uses backtracking, but does not use an extended set.
    """
    #go on left most
    #find the neighbors of that
    #backtracks by the popping off queue
    
    
    queue1 = [startNode]
    print(queue1)
    queue= extensions(graph, queue1) #acts funny with the first iteration so I added neigbors to start node outside the loop
    print(queue)
    while len(queue)>0:
        front = queue.pop(0) #pops first thing off the queue
        
        extension = extensions(graph, front) #extends it
        extension.reverse() #order matters
        
        #extension gives a list of lists so want to add each list to queue so it doesn't act weird
        for path in range(0,len(extension)):
            queue.insert(0, extension[path]) #adds it to the front of the queue
        
        #if we went through the whole queue and still couldn't find the path
        if len(queue) ==0:
            return None
        
        elif queue[0][-1] == goalNode: #checks to see if at goal node
            return queue[0]
        



def basic_bfs(graph, startNode, goalNode):
    """
    Performs a breadth-first search on a graph from a specified start
    node to a specified goal node, returning a path-to-goal if it
    exists, otherwise returning None.
    """
    
    #did I do bfs right? we don't do any popping right?
    
    extended_list = [startNode]
    queue1 = [startNode]
    queue= extensions(graph, queue1)
    #print('queue', queue)
    path_to_goal = []
    
    #tranverse horizontally
    while len(queue)>0:
        
        temp_queue = []
        
        #extends the last of each node
        for path in queue:
            extension = extensions(graph,path) 
            for path in extension: #have to do this so it doesn't act weird
                
                temp_queue.append(path)
        
        queue = []
        
        #adds to the queue horizontally if neighbor is not in the extended list
        for path in temp_queue:
            if path[-1] not in extended_list: 
                queue.append(path) #updates the queue with the extended paths
                extended_list.append(path[-1])  #keeps track of the letters
                if path[-1] == goalNode: #path to gaol
                    path_to_goal.append(path)
                    
        
        
    # if no path to goal, return none
    if len(path_to_goal) ==0:
        return None
    
    
    return path_to_goal[0]
    
    

#### PART 3: Generic Search ####################################################

# Generic search requires four arguments (see wiki for more details):
    

# def sort_new_paths_fn(graph, goalNode, new_paths): 
# add_paths_to_front_of_agenda: True if new paths should be added to the front of the agenda
# sort_agenda_fn: function to sort the agenda after adding all new paths 
# use_extended_set: True if the algorithm should utilize an extended set

# Define your custom path-sorting functions here.
# Each path-sorting function should be in this form:
def sort_path_by_heuristic(graph, goalNode, new_paths):
    '''
    sorts paths by heuristic of last node in path
    '''
    new_paths_c = new_paths.copy()
    new_paths_c.sort()
    sorted_paths = sorted(new_paths_c, key=lambda path: graph.get_heuristic_value(path[-1], goalNode))
    return sorted_paths

def sort_path_by_length(graph, goalNode, new_paths):
    '''
    sort paths by path length
    '''
    new_paths_c = new_paths.copy()
    new_paths_c.sort()
    sorted_paths = sorted(new_paths_c, key=lambda path: path_length(graph, path))
    return sorted_paths

def sort_agenda_fn(graph, goalNode, agenda_paths):
    ''' sorts whole agenda'''
    agenda_paths_c = agenda_paths.copy()
    agenda_paths_c.sort()
    sorted_paths = sorted(agenda_paths_c, key=lambda path: graph.get_heuristic_value(path[-1], goalNode))
    return sorted_paths

def sort_length_and_heuristic(graph, goalNode, new_paths):
    '''sorts by length and heuristic'''
    new_paths_copy = new_paths.copy()
    new_paths_copy.sort()
    
    sorted_heur = sorted(new_paths_copy, key=lambda path: graph.get_heuristic_value(path[-1], goalNode)+ path_length(graph, path))
    
    
    return sorted_heur


def break_ties(paths):
    raise NotImplementedError
    return sorted(paths)

generic_dfs = [do_nothing_fn, True, do_nothing_fn, False]

generic_bfs = [do_nothing_fn, False, do_nothing_fn, False]

generic_hill_climbing = [sort_path_by_heuristic, True, do_nothing_fn, False]

generic_best_first = [do_nothing_fn, True, sort_agenda_fn, False]

generic_branch_and_bound = [do_nothing_fn, False, sort_path_by_length, False]

generic_branch_and_bound_with_heuristic = [do_nothing_fn, False, sort_length_and_heuristic, False]

generic_branch_and_bound_with_extended_set = [do_nothing_fn, False, sort_path_by_length, True]

generic_a_star = [do_nothing_fn, False, sort_length_and_heuristic, True]

# Here is an example of how to call generic_search (uncomment to run):
# my_dfs_fn = generic_search(*generic_dfs)
# my_dfs_path = my_dfs_fn(GRAPH_2, 'S', 'G')
# print(my_dfs_path)

# Or, combining the first two steps:
# my_dfs_path = generic_search(*generic_dfs)(GRAPH_2, 'S', 'G')
# print(my_dfs_path)


### OPTIONAL: Generic Beam Search

# If you want to run local tests for generic_beam, change TEST_GENERIC_BEAM to True:
TEST_GENERIC_BEAM = False

# The sort_agenda_fn for beam search takes fourth argument, beam_width:
# def my_beam_sorting_fn(graph, goalNode, paths, beam_width):
#     # YOUR CODE HERE
#     return sorted_beam_agenda

generic_beam = [None, None, None, None]


# Uncomment this to test your generic_beam search:
# print(generic_search(*generic_beam)(GRAPH_2, 'S', 'G', beam_width=2))


#### PART 4: Heuristics ########################################################

def is_admissible(graph, goalNode):
    """Returns True if this graph's heuristic is admissible; else False.
    A heuristic is admissible if it is either always exactly correct or overly
    optimistic; it never over-estimates the cost to the goal."""
    
    all_nodes = graph.nodes
    
    for node in range(0,len(all_nodes)-1): #-1 so it doesn't count goal node?
        #finds the shortest path b/w node and goal
        shortest_path = generic_search(*generic_bfs)(graph, all_nodes[node], goalNode)#figure this out later
        #finds path_length to compare heuristic against
        path_lengths = path_length(graph, shortest_path)
        
        if graph.get_heuristic_value(all_nodes[node], goalNode)>path_lengths:
            
            return False
            
    
    return True

def is_consistent(graph, goalNode):
    """Returns True if this graph's heuristic is consistent; else False.
    A consistent heuristic satisfies the following property for all
    nodes v in the graph:
        Suppose v is a node in the graph, and N is a neighbor of v,
        then, heuristic(v) <= heuristic(N) + edge_weight(v, N)
    In other words, moving from one node to a neighboring node never unfairly
    decreases the heuristic.
    This is equivalent to the heuristic satisfying the triangle inequality."""
    
    all_nodes = graph.nodes
    
    for node in range(0,len(all_nodes)-1):
        neighbors = graph.get_neighbors(all_nodes[node])
        
        for neighbor in range(0,len(neighbors)):
            edge = graph.get_edge(all_nodes[node], neighbors[neighbor])
            
           
            
            edge_w= edge.length #edge weight
            
            #heur_diff is the heur of the node - heur of neighbor
            heur_diff = abs(graph.get_heuristic_value(all_nodes[neighbor], goalNode) -graph.get_heuristic_value(all_nodes[node], goalNode))
            
            
            if heur_diff >edge_w:
                    
                return False
    
    return True
    
    

### OPTIONAL: Picking Heuristics

# If you want to run local tests on your heuristics, change TEST_HEURISTICS to True.
#  Note that you MUST have completed generic a_star in order to do this:
TEST_HEURISTICS = False


# heuristic_1: admissible and consistent

[h1_S, h1_A, h1_B, h1_C, h1_G] = [None, None, None, None, None]

heuristic_1 = {'G': {}}
heuristic_1['G']['S'] = h1_S
heuristic_1['G']['A'] = h1_A
heuristic_1['G']['B'] = h1_B
heuristic_1['G']['C'] = h1_C
heuristic_1['G']['G'] = h1_G


# heuristic_2: admissible but NOT consistent

[h2_S, h2_A, h2_B, h2_C, h2_G] = [None, None, None, None, None]

heuristic_2 = {'G': {}}
heuristic_2['G']['S'] = h2_S
heuristic_2['G']['A'] = h2_A
heuristic_2['G']['B'] = h2_B
heuristic_2['G']['C'] = h2_C
heuristic_2['G']['G'] = h2_G


# heuristic_3: admissible but A* returns non-optimal path to G

[h3_S, h3_A, h3_B, h3_C, h3_G] = [None, None, None, None, None]

heuristic_3 = {'G': {}}
heuristic_3['G']['S'] = h3_S
heuristic_3['G']['A'] = h3_A
heuristic_3['G']['B'] = h3_B
heuristic_3['G']['C'] = h3_C
heuristic_3['G']['G'] = h3_G


# heuristic_4: admissible but not consistent, yet A* finds optimal path

[h4_S, h4_A, h4_B, h4_C, h4_G] = [None, None, None, None, None]

heuristic_4 = {'G': {}}
heuristic_4['G']['S'] = h4_S
heuristic_4['G']['A'] = h4_A
heuristic_4['G']['B'] = h4_B
heuristic_4['G']['C'] = h4_C
heuristic_4['G']['G'] = h4_G


##### PART 5: Multiple Choice ##################################################

ANSWER_1 = '2' #British Museum?

ANSWER_2 = '4' #Branch and Bound with Extended Set

ANSWER_3 = '1' #Breath First Search

ANSWER_4 = '3' #A*


#### SURVEY ####################################################################

NAME = 'Athena Nguyen'
COLLABORATORS = 'Elina '
HOW_MANY_HOURS_THIS_LAB_TOOK = '10'
WHAT_I_FOUND_INTERESTING = 'figuring out the algorithms'
WHAT_I_FOUND_BORING = 'None'
SUGGESTIONS = None



###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

# The following lines are used in the online tester. DO NOT CHANGE!

generic_dfs_sort_new_paths_fn = generic_dfs[0]
generic_bfs_sort_new_paths_fn = generic_bfs[0]
generic_hill_climbing_sort_new_paths_fn = generic_hill_climbing[0]
generic_best_first_sort_new_paths_fn = generic_best_first[0]
generic_branch_and_bound_sort_new_paths_fn = generic_branch_and_bound[0]
generic_branch_and_bound_with_heuristic_sort_new_paths_fn = generic_branch_and_bound_with_heuristic[0]
generic_branch_and_bound_with_extended_set_sort_new_paths_fn = generic_branch_and_bound_with_extended_set[0]
generic_a_star_sort_new_paths_fn = generic_a_star[0]

generic_dfs_sort_agenda_fn = generic_dfs[2]
generic_bfs_sort_agenda_fn = generic_bfs[2]
generic_hill_climbing_sort_agenda_fn = generic_hill_climbing[2]
generic_best_first_sort_agenda_fn = generic_best_first[2]
generic_branch_and_bound_sort_agenda_fn = generic_branch_and_bound[2]
generic_branch_and_bound_with_heuristic_sort_agenda_fn = generic_branch_and_bound_with_heuristic[2]
generic_branch_and_bound_with_extended_set_sort_agenda_fn = generic_branch_and_bound_with_extended_set[2]
generic_a_star_sort_agenda_fn = generic_a_star[2]

# Creates the beam search using generic beam args, for optional beam tests
beam = generic_search(*generic_beam) if TEST_GENERIC_BEAM else None

# Creates the A* algorithm for use in testing the optional heuristics
if TEST_HEURISTICS:
    a_star = generic_search(*generic_a_star)
