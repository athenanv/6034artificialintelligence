# MIT 6.034 Lab 7: Neural Nets
# Written by 6.034 Staff

from nn_problems import *
from math import e
INF = float('inf')


#### Part 1: Wiring a Neural Net ###############################################

nn_half = [1]

nn_angle = [2,1]

nn_cross = [2,2,1]

nn_stripe = [3,1]

nn_hexagon = [6,1]

nn_grid = [4,2,1]


#### Part 2: Coding Warmup #####################################################

# Threshold functions
def stairstep(x, threshold=0):
    "Computes stairstep(x) using the given threshold (T)"
    if x >=threshold:
        return 1
    else:
        return 0

def sigmoid(x, steepness=1, midpoint=0):
    "Computes sigmoid(x) using the given steepness (S) and midpoint (M)"
    return 1/(1+e**(-steepness*(x-midpoint)))

def ReLU(x):
    "Computes the threshold of an input using a rectified linear unit."
    return max(0,x)

# Accuracy function
def accuracy(desired_output, actual_output):
    "Computes accuracy. If output is binary, accuracy ranges from -0.5 to 0."
    
    return -0.5*(desired_output-actual_output)**2


#### Part 3: Forward Propagation ###############################################

def node_value(node, input_values, neuron_outputs):  # PROVIDED BY THE STAFF
    """
    Given 
     * a node (as an input or as a neuron),
     * a dictionary mapping input names to their values, and
     * a dictionary mapping neuron names to their outputs
    returns the output value of the node.
    This function does NOT do any computation; it simply looks up
    values in the provided dictionaries.
    """
    if isinstance(node, str):
        # A string node (either an input or a neuron)
        if node in input_values:
            return input_values[node]
        if node in neuron_outputs:
            return neuron_outputs[node]
        raise KeyError("Node '{}' not found in either the input values or neuron outputs dictionary.".format(node))
    
    if isinstance(node, (int, float)):
        # A constant input, such as -1
        return node
    
    raise TypeError("Node argument is {}; should be either a string or a number.".format(node))

def forward_prop(net, input_values, threshold_fn=stairstep):
    """Given a neural net and dictionary of input values, performs forward
    propagation with the given threshold function to compute binary output.
    This function should not modify the input net.  Returns a tuple containing:
    (1) the final output of the neural net
    (2) a dictionary mapping neurons to their immediate outputs"""
    
    sorted_net = net.topological_sort()
    neuron_dict = {}
    for node in sorted_net:
        inputs = net.get_incoming_neighbors(node)
        weighted_inputs = 0
        for i in inputs:
            wire = net.get_wires(i, node)[0]
            if type(i) is int:
                weighted_inputs += i*wire.get_weight()
            else:
                weighted_inputs += input_values[i]*wire.get_weight()
        neuron_dict[node] = threshold_fn(weighted_inputs)
        if node == net.get_output_neuron():
            return(neuron_dict[node], neuron_dict)
        if node not in input_values.keys():
            input_values[node] = node_value(node, input_values, neuron_dict)


#### Part 4: Backward Propagation ##############################################
def combinations(inputs, step_size):
    ''' make combinations keeping 1 index the same 
    Returns (lists, index held constant'''
    len_inputs = len(inputs)
    list_of_inputs = []
    inputs_c = inputs.copy()
    for index in range(len_inputs):
        plus_step = inputs_c.copy()
        plus_step[index] = plus_step[index] +step_size
        list_of_inputs.append((plus_step,[index]))
        minus_step = inputs_c.copy()
        minus_step[index] = minus_step[index] -step_size
        list_of_inputs.append((minus_step, [index]))
    return list_of_inputs

def combinations_2(possibilities, step_size):
    ''' make combinations keeping 2 indices the same
    Returns (lists, indices held constant'''
    list_of_inputs = possibilities.copy()
    just_lists = [pos[0] for pos in possibilities]
    for triplet, index in possibilities:
        for num in range(len(triplet)):
            if num == index[0]:
                continue
            triplet_plus = triplet.copy()
            triplet_plus[num] = triplet_plus[num] + step_size
            if triplet_plus not in just_lists:
                just_lists.append(triplet_plus)
                list_of_inputs.append((triplet_plus, [index[0],num]))
            triplet_minus = triplet.copy()
            triplet_minus[num] = triplet_minus[num] - step_size
            if triplet_minus not in just_lists:
                just_lists.append(triplet_minus)
                list_of_inputs.append((triplet_minus,[index[0],num]))
    return list_of_inputs

def gradient_ascent_step(func, inputs, step_size):
    """Given an unknown function of three variables and a list of three values
    representing the current inputs into the function, increments each variable
    by +/- step_size or 0, with the goal of maximizing the function output.
    After trying all possible variable assignments, returns a tuple containing:
    (1) the maximum function output found, and
    (2) the list of inputs that yielded the highest function output."""
    possibilities = combinations(inputs, step_size)
    list_of_inputs_2 =combinations_2(possibilities, step_size)
    list_of_inputs_3 = [pos[0] for pos in list_of_inputs_2]
    for triplet, index in list_of_inputs_2: #this changes the value at the only index not altered yet
        for num in range(len(triplet)):
            if num in index:
                continue
            triplet_plus = triplet.copy()
            triplet_plus[num] = triplet_plus[num] + step_size
            if triplet_plus not in list_of_inputs_3:
                list_of_inputs_3.append(triplet_plus)
            triplet_minus = triplet.copy()
            triplet_minus[num] = triplet_minus[num] - step_size
            if triplet_minus not in list_of_inputs_3:
                list_of_inputs_3.append(triplet_minus)
    list_of_inputs_3.append(inputs)
    highest = -INF
    for inp in list_of_inputs_3:
        if func(inp[0], inp[1], inp[2]) > highest:
            highest = func(inp[0], inp[1], inp[2])
            best_inp = inp
    return (highest, best_inp)


def get_back_prop_dependencies(net, wire):
    """Given a wire in a neural network, returns a set of inputs, neurons, and
    Wires whose outputs/values are required to update this wire's weight."""

    dependency_set = set()
    back_prop_queue = [wire]
    while len(back_prop_queue) >0:
        current_wire = back_prop_queue.pop(0)
        
        dependency_set.add(current_wire)
        dependency_set.add(current_wire.startNode)
        node_b = current_wire.endNode
        back_prop_queue.extend(net.get_wires(node_b))
        dependency_set.add(node_b)
        if len(net.get_outgoing_neighbors(node_b)) != 0:
            for node in net.get_outgoing_neighbors(node_b):
                
                back_prop_queue.extend(net.get_wires(node))    
    return dependency_set
  
        

def calculate_deltas(net, desired_output, neuron_outputs):
    """Given a neural net and a dictionary of neuron outputs from forward-
    propagation, computes the update coefficient (delta_B) for each
    neuron in the net. Uses the sigmoid function to compute neuron output.
    Returns a dictionary mapping neuron names to update coefficient (the
    delta_B values). """
    updated_deltas = {}
    sorted_nodes = net.topological_sort()
    sorted_nodes.reverse()
    for neuron in sorted_nodes:
        out_b = neuron_outputs[neuron]
        if neuron == net.get_output_neuron():
            updated_deltas[neuron] = out_b*(1-out_b)*(desired_output-out_b)
        else:
            sum_w = 0
            outgoing_wires = net.get_wires(neuron)
            for wire in outgoing_wires:
                sum_w += updated_deltas[wire.endNode]*wire.get_weight()
            updated_deltas[neuron] = out_b*(1-out_b)*sum_w      
    return updated_deltas


def update_weights(net, input_values, desired_output, neuron_outputs, r=1):
    """Performs a single step of back-propagation.  Computes delta_B values and
    weight updates for entire neural net, then updates all weights.  Uses the
    sigmoid function to compute neuron output.  Returns the modified neural net,
    with the updated weights."""
    deltas = calculate_deltas(net, desired_output, neuron_outputs)
    for wire in net.get_wires():
        old = wire.get_weight()
        delta_B = deltas[wire.endNode]
        if wire.startNode in input_values.keys():
            if type(wire.startNode) is int:
                new = old + r*delta_B*wire.startNode
            else:
                new = old + r*delta_B*input_values[wire.startNode]
        else:
             if type(wire.startNode) is int:
                new = old + r*delta_B*wire.startNode
             else:
                new = old + r*delta_B*neuron_outputs[wire.startNode]
        wire.set_weight(new)
    return net

def back_prop(net, input_values, desired_output, r=1, minimum_accuracy=-0.001):
    """Updates weights until accuracy surpasses minimum_accuracy.  Uses the
    sigmoid function to compute neuron output.  Returns a tuple containing:
    (1) the modified neural net, with trained weights
    (2) the number of iterations (that is, the number of weight updates)"""
    forward = forward_prop(net, input_values, sigmoid)
    iterations = 0
    accuracy_fraction = accuracy(desired_output, forward[0])
    while accuracy_fraction < minimum_accuracy:
        update_weights(net, input_values, desired_output, forward[1], r)
        iterations += 1
        forward = forward_prop(net, input_values, sigmoid)
        accuracy_fraction = accuracy(desired_output, forward[0])
        
    return (net, iterations)
    
    


#### Part 5: Training a Neural Net #############################################

ANSWER_1 = 25
ANSWER_2 = 29
ANSWER_3 = 2
ANSWER_4 = 333
ANSWER_5 = 31

ANSWER_6 = 1
ANSWER_7 = 'checkerboard'
ANSWER_8 = ['small', 'medium', 'large']
ANSWER_9 = 'B'

ANSWER_10 = 'D'
ANSWER_11 =['A', 'C']
ANSWER_12 = ['A', 'E']


#### SURVEY ####################################################################

NAME = 'Athena Nguyen'
COLLABORATORS = 'Somaia Saba, Ryan Mansilla, Leilani Trautman, Haldrian'
HOW_MANY_HOURS_THIS_LAB_TOOK = '15'
WHAT_I_FOUND_INTERESTING = None
WHAT_I_FOUND_BORING = None
SUGGESTIONS = None
