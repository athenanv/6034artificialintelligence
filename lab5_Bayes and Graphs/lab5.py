# MIT 6.034 Lab 5: Bayesian Inference
# Written by 6.034 staff

from nets import *


#### Part 1: Warm-up; Ancestors, Descendents, and Non-descendents ##############

def get_ancestors(net, var):
    "Return a set containing the ancestors of var"
    parents = list(net.get_parents(var))
    
    ancestors = []
    while len(parents) > 0:
        next_parent = parents.pop(0)
        ancestors.append(next_parent)
        if len(list(net.get_parents(next_parent))) == 0:
            continue
        else:
            parents = parents + list(net.get_parents(next_parent))
    
    return set(ancestors)

def get_descendants(net, var):
    "Returns a set containing the descendants of var"
    children = list(net.get_children(var))
    
    descendants = []
    while len(children) > 0:
        next_child = children.pop(0)
        descendants.append(next_child)
        if len(list(net.get_children(next_child))) == 0:
            continue
        children = children + list(net.get_children(next_child))
    return set(descendants)

def get_nondescendants(net, var):
    "Returns a set containing the non-descendants of var"
    variables = net.get_variables()
    variables.remove(var)
    descendants = list(get_descendants(net, var))
    nondescendants = [v for v in variables if v not in descendants]
    return set(nondescendants)


#### Part 2: Computing Probability #############################################

def simplify_givens(net, var, givens):
    """
    If givens include every parent of var and no descendants, returns a
    simplified list of givens, keeping only parents.  Does not modify original
    givens.  Otherwise, if not all parents are given, or if a descendant is
    given, returns original givens.
    """
    parent_count = 0
    parents = net.get_parents(var)
    for given in givens:
        if given in get_descendants(net, var):
            return givens
        if given in parents:
            parent_count += 1
    if parent_count == len(parents):
        
        simplified_givens = {givens_key: givens[givens_key] for givens_key in givens.keys() if givens_key in parents}
        return simplified_givens
    
    return givens
    
def probability_lookup(net, hypothesis, givens=None):
    "Looks up a probability in the Bayes net, or raises LookupError"
    
    if givens is not None:
        
        for hypothesis_key in hypothesis.keys():
            var = hypothesis_key
        simplified_givens = simplify_givens(net, var, givens)
        try:
            return net.get_probability(hypothesis, simplified_givens)
        except ValueError:
            raise LookupError
    elif givens is None:
        try:
            return net.get_probability(hypothesis, givens)
        except ValueError:
            raise LookupError

def probability_joint(net, hypothesis):
    "Uses the chain rule to compute a joint probability"
    hypothesis_copy = hypothesis.copy()
    sorted_vars = net.topological_sort(hypothesis_copy)
    sorted_vars.reverse()
    new_hypothesis = {sort_key:hypothesis[sort_key] for sort_key in sorted_vars}
    probability = 1
    while len(sorted_vars) > 0:
        key = sorted_vars.pop(0)
        key_value = hypothesis[key]
        new_hypothesis.pop(key)
        try:
            probability *=probability_lookup(net, {key:key_value}, new_hypothesis)
        except LookupError:
            continue
   
    return probability
        
    
def probability_marginal(net, hypothesis):
    "Computes a marginal probability as a sum of joint probabilities"
    probability = 0
    combinations = net.combinations(net.variables, hypothesis)
    for combo in combinations:
        probability += probability_joint(net, combo)

    return probability

def probability_conditional(net, hypothesis, givens=None):
    "Computes a conditional probability as a ratio of marginal probabilities"
    
    if givens is None:
        conditional = probability_joint(net, hypothesis)
    else:
        for key in hypothesis.keys():
            if key in givens.keys():
                if hypothesis[key] != givens[key]:
                    return 0
        hypothesis_givens = dict(hypothesis, **givens) #combines the dictionaries
        conditional = probability_marginal(net, hypothesis_givens)/probability_marginal(net, givens)
    return conditional
    
def probability(net, hypothesis, givens=None):
    "Calls previous functions to compute any probability"
    if givens is None:
        if len(net.get_variables())==len(list(hypothesis.keys())): #joint if hypothesis has all variables
            return probability_joint(net, hypothesis)
        elif len(net.get_variables())>len(list(hypothesis.keys())): #marginal if hypothesis has an incomplete set of variables in the net
            return probability_marginal(net,hypothesis)
    else:
        return probability_conditional(net, hypothesis, givens)


#### Part 3: Counting Parameters ###############################################

def number_of_parameters(net):
    """
    Computes the minimum number of parameters required for the Bayes net.
    """
    
    domains_len = []
   
    for var in net.variables:
        domain_len = len(net.get_domain(var))
        
        domains_len.append(domain_len**(len(net.get_parents(var))))
    
    return sum(domains_len)


#### Part 4: Independence ######################################################

def is_independent(net, var1, var2, givens=None):
    """
    Return True if var1, var2 are conditionally independent given givens,
    otherwise False. Uses numerical independence.
    """
    
    if givens is None:
        
        for value in net.get_domain(var1):
            for v in net.get_domain(var2):
                
                try:
                    
                    p_a = probability_lookup(net, {var1: value})
                    hyp = {var1: value, var2:v}
                    conditional = probability_conditional(net, hyp, {var2:v})
                    if not approx_equal(p_a, conditional, epsilon=0.0000000001):
                        return False
                except LookupError:
                    
                    continue
        return True
    else:
        
        var2_domain =net.get_domain(var2)
        givens_copy = givens.copy()
        new_dicts = [dict({var2:value}, **givens_copy) for value in var2_domain]
        for value in net.get_domain(var1):
            for dictionary in new_dicts:
                conditional_1 = probability_conditional(net,{var1:value}, givens)
                conditional_2 = probability_conditional(net,{var1:value}, dictionary)
                if not approx_equal(conditional_1, conditional_2, epsilon=0.0000000001):
                    return False
        return True
        
    
def pairs_of_variables(variables):
     '''generates all possible pairs of variables'''
     pairs_of_variables = []
     var_c = list(variables.copy())
     while len(var_c) >0:
         first_var = var_c.pop(0)
         for var in var_c:
             pairs_of_variables.append([first_var, var])
     return pairs_of_variables 
    
def is_structurally_independent(net, var1, var2, givens=None):
    """
    Return True if var1, var2 are conditionally independent given givens,
    based on the structure of the Bayes net, otherwise False.
    Uses structural independence only (not numerical independence).
    """
    
    
    #draw ancestral graph
    ancestral_graph_vars = list(get_ancestors(net, var1).union(get_ancestors(net, var2)))+[var1,var2]
    if givens is not None: 
        ancestral_graph_vars = ancestral_graph_vars + list(givens) 
        for given in givens:
            ancestral_graph_vars.extend(list(get_ancestors(net, given)))
    ancestral_graph_vars = set(ancestral_graph_vars)
    ancestral_graph_vars= list(ancestral_graph_vars)
    subnet = net.subnet(ancestral_graph_vars)
    
    #connect each set of parents
    
    
    parents_vars = list(subnet.get_parents(var1))
    # pairs = pairs_of_variables(parents_vars)
    for pair in range(len(parents_vars)-1):
        subnet.link(parents_vars[pair], parents_vars[pair+1])
    parents_vars2 = list(subnet.get_parents(var2))
    pairs2 = pairs_of_variables(parents_vars2)
    
    for pair in range(len(parents_vars2)-1):
        subnet.link(parents_vars2[pair], parents_vars2[pair+1])
    
    if givens is not None:
        for given in givens:
            parents_vars3 = list(subnet.get_parents(given))
            pairs3 = pairs_of_variables(parents_vars3)
            for pair in range(len(parents_vars3)-1):
                subnet.link(parents_vars3[pair], parents_vars3[pair+1])
   
    #make graphs undirected
    subnet.make_bidirectional()
    
    #delete givens and their edges
    if givens is not None:  
        for given in givens.keys():
            subnet.remove_variable(given)
            
    #read the graph
   
    if subnet.find_path(var1, var2) is None:
        return True
    else:
        return False


#### SURVEY ####################################################################

NAME = 'Athena Nguyen'
COLLABORATORS = 'Ryan Mansilla, Somaia Saba '
HOW_MANY_HOURS_THIS_LAB_TOOK = '10'
WHAT_I_FOUND_INTERESTING = None
WHAT_I_FOUND_BORING = None
SUGGESTIONS = None
