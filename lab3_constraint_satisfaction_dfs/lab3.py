# MIT 6.034 Lab 3: Constraint Satisfaction Problems
# Written by 6.034 staff

from constraint_api import *
from test_problems import get_pokemon_problem


#### Part 1: Warmup ############################################################

def has_empty_domains(csp) :
    """Returns True if the problem has one or more empty domains, otherwise False"""
    
    variables = csp.get_all_variables()
    for var in variables:
        if len(csp.get_domain(var)) == 0:
            return True
    return False
def check_all_constraints(csp) :
    """Return False if the problem's assigned values violate some constraint,
    otherwise True"""
    constraints = csp.get_all_constraints()
    
    for constraint in constraints:
        
        # if a variable no constraints then continue
        if csp.get_assignment(constraint.var1) is None or csp.get_assignment(constraint.var2) is None:
            continue
        #if violate a constraint, then return False
        if not constraint.check(csp.get_assignment(constraint.var1), csp.get_assignment(constraint.var2)):
            return False
    return True


#### Part 2: Depth-First Constraint Solver #####################################

def solve_constraint_dfs(problem) :
    """
    Solves the problem using depth-first search.  Returns a tuple containing:
    1. the solution (a dictionary mapping variables to assigned values)
    2. the number of extensions made (the number of problems popped off the agenda).
    If no solution was found, return None as the first element of the tuple.
    """
    problem_copy = problem.copy()
    
    extensions = 0
    queue = [problem_copy]
    # #performs dfs on each node
    #while len(queue)>0:
    while len(queue) >0:
        next_problem = queue.pop(0)
        
        extensions += 1
        if has_empty_domains(next_problem):
            continue
        
        if check_all_constraints(next_problem) and len(next_problem.unassigned_vars) == 0:
            return(next_problem.assignments, extensions)
        
        if len(next_problem.unassigned_vars) == 0:
            #if there are no more variables to assign, just want to keep iterating through queue until find a path that satisfies
            continue
        
        #extends the queue by adding the previous problem + the next unassigned variable and the possible assignments of that unassigned variable
        next_unassigned_var = next_problem.pop_next_unassigned_var()
        unassigned_domain = next_problem.get_domain(next_unassigned_var)
        
        new_problems = []
        for assig in unassigned_domain:
            problem_to_add_to_queue = next_problem.copy()
            if check_all_constraints(problem_to_add_to_queue):
                
                problem_to_add_to_queue.set_assignment(next_unassigned_var, assig)
            
                new_problems.append(problem_to_add_to_queue)
        
        queue = new_problems + queue
        
        
    return (None, extensions)


# QUESTION 1: How many extensions does it take to solve the Pokemon problem
#    with DFS?

# Hint: Use get_pokemon_problem() to get a new copy of the Pokemon problem
#    each time you want to solve it with a different search method.

ANSWER_1 = solve_constraint_dfs(get_pokemon_problem())[1]


#### Part 3: Forward Checking ##################################################

def violations_in_neighbor(csp, var, neighbor):
    '''returns a list of the violations of the values in the
    neighbor of current var according to the constraints'''
    values_in_violation = []
    var_domain = csp.get_domain(var)
    neighbor_domain = csp.get_domain(neighbor)
    constraint = csp.constraints_between(var, neighbor)
    
    for neighbor_assig in neighbor_domain:
        violations_counter = 0
        for var_assignment in var_domain:
            for con in constraint:
                if not con.check(neighbor_assig, var_assignment):
                    
                    violations_counter += 1
                    if violations_counter == len(var_domain):
                        values_in_violation.append(neighbor_assig)
    return values_in_violation
    
def eliminate_from_neighbors(csp, var) :
    """
    Eliminates incompatible values from var's neighbors' domains, modifying
    the original csp.  Returns an alphabetically sorted list of the neighboring
    variables whose domains were reduced, with each variable appearing at most
    once.  If no domains were reduced, returns empty list.
    If a domain is reduced to size 0, quits immediately and returns None.
    """
    neighbors = csp.get_neighbors(var)
    reduced_var =[]
    for neigh in neighbors:
        violations_list = violations_in_neighbor(csp, var, neigh)
        if len(violations_list)!=0:
            for value in violations_list:
                csp.eliminate(neigh, value)
            reduced_var.append(neigh)
            if len(csp.get_domain(neigh)) ==0:
                return None
        
    return sorted(reduced_var)

# Because names give us power over things (you're free to use this alias)
forward_check = eliminate_from_neighbors

def solve_constraint_forward_checking(problem) :
    """
    Solves the problem using depth-first search with forward checking.
    Same return type as solve_constraint_dfs.
    """
    problem_copy = problem.copy()
    
    extensions = 0
    queue = [problem_copy]
    # #performs dfs on each node
    #while len(queue)>0:
    while len(queue) >0:
        next_problem = queue.pop(0)
        
        extensions += 1
        if has_empty_domains(next_problem):
            continue
        
        if check_all_constraints(next_problem) and len(next_problem.unassigned_vars) == 0:
            return(next_problem.assignments, extensions)
        
        if len(next_problem.unassigned_vars) == 0:
            #if there are no more variables to assign, just want to keep iterating through queue until find a path that satisfies
            continue
        
        #extends the queue by adding the previous problem + the next unassigned variable and the possible assignments of that unassigned variable
        next_unassigned_var = next_problem.pop_next_unassigned_var()
        unassigned_domain = next_problem.get_domain(next_unassigned_var)
        
        new_problems = []
        for assig in unassigned_domain:
            problem_to_add_to_queue = next_problem.copy()
            if check_all_constraints(problem_to_add_to_queue):
                
                problem_to_add_to_queue.set_assignment(next_unassigned_var, assig)
                eliminate_from_neighbors(problem_to_add_to_queue, next_unassigned_var)
                new_problems.append(problem_to_add_to_queue)
        
        queue = new_problems + queue
        
        
    return (None, extensions)


# QUESTION 2: How many extensions does it take to solve the Pokemon problem
#    with DFS and forward checking?

ANSWER_2 = solve_constraint_forward_checking(get_pokemon_problem())[1]


#### Part 4: Domain Reduction ##################################################

def domain_reduction(csp, queue=None) :
    """
    Uses constraints to reduce domains, propagating the domain reduction
    to all neighbors whose domains are reduced during the process.
    If queue is None, initializes propagation queue by adding all variables in
    their default order. 
    Returns a list of all variables that were dequeued, in the order they
    were removed from the queue.  Variables may appear in the list multiple times.
    If a domain is reduced to size 0, quits immediately and returns None.
    This function modifies the original csp.
    """
    var_dequeued = []
    if queue is None:
        prop_queue = csp.get_all_variables()
    else:
        prop_queue = queue
    
    while len(prop_queue) >0:
        next_var = prop_queue.pop(0)
        var_dequeued.append(next_var)

        eliminated = eliminate_from_neighbors(csp, next_var)
        if eliminated is None:
            return None
        prop_queue = prop_queue + eliminated
        
            
    return var_dequeued


# QUESTION 3: How many extensions does it take to solve the Pokemon problem
#    with DFS (no forward checking) if you do domain reduction before solving it?
q3_pokemon = get_pokemon_problem()
domain_reduction(q3_pokemon, queue=None)

ANSWER_3 = solve_constraint_dfs(q3_pokemon)[1]


def solve_constraint_propagate_reduced_domains(problem) :
    """
    Solves the problem using depth-first search with forward checking and
    propagation through all reduced domains.  Same return type as
    solve_constraint_dfs.
    """
    problem_copy = problem.copy()
    
    extensions = 0
    queue = [problem_copy]
    # #performs dfs on each node
    #while len(queue)>0:
    while len(queue) >0:
        next_problem = queue.pop(0)
        
        extensions += 1
        if has_empty_domains(next_problem):
            continue
        
        if check_all_constraints(next_problem) and len(next_problem.unassigned_vars) == 0:
            return(next_problem.assignments, extensions)
        
        if len(next_problem.unassigned_vars) == 0:
            #if there are no more variables to assign, just want to keep iterating through queue until find a path that satisfies
            continue
        
        #extends the queue by adding the previous problem + the next unassigned variable and the possible assignments of that unassigned variable
        next_unassigned_var = next_problem.pop_next_unassigned_var()
        unassigned_domain = next_problem.get_domain(next_unassigned_var)
        
        new_problems = []
        for assig in unassigned_domain:
            problem_to_add_to_queue = next_problem.copy()
            if check_all_constraints(problem_to_add_to_queue):
                
                problem_to_add_to_queue.set_assignment(next_unassigned_var, assig)
                queue.append(next_unassigned_var)
                domain_reduction(problem_to_add_to_queue, queue)
                new_problems.append(problem_to_add_to_queue)
        
        queue = new_problems + queue
        
        
    return (None, extensions)


# QUESTION 4: How many extensions does it take to solve the Pokemon problem
#    with forward checking and propagation through reduced domains?

ANSWER_4 = solve_constraint_propagate_reduced_domains(get_pokemon_problem())[1]


#### Part 5A: Generic Domain Reduction #########################################

def propagate(enqueue_condition_fn, csp, queue=None) :
    """
    Uses constraints to reduce domains, modifying the original csp.
    Uses enqueue_condition_fn to determine whether to enqueue a variable whose
    domain has been reduced. Same return type as domain_reduction.
    """
    var_dequeued = []
    if queue is None:
        prop_queue = csp.get_all_variables()
    else:
        prop_queue = queue
    
    while len(prop_queue) >0:
        next_var = prop_queue.pop(0)
        var_dequeued.append(next_var)

        eliminated = eliminate_from_neighbors(csp, next_var)
        if eliminated is None:
            return None
        # if enqueue_condition_fn is None:
        #     prop_queue = prop_queue + eliminated
        # else:
        for var in eliminated:
            
            if enqueue_condition_fn(csp,var) or enqueue_condition_fn(csp,var) is None:
                prop_queue.append(var)
        
            
    return var_dequeued

def condition_domain_reduction(csp, var) :
    """Returns True if var should be enqueued under the all-reduced-domains
    condition, otherwise False"""
    
    return True

def condition_singleton(csp, var) :
    """Returns True if var should be enqueued under the singleton-domains
    condition, otherwise False"""
    if len(csp.get_domain(var)) == 1:
        return True
    return False

def condition_forward_checking(csp, var) :
    """Returns True if var should be enqueued under the forward-checking
    condition, otherwise False"""
    return False


#### Part 5B: Generic Constraint Solver ########################################

def solve_constraint_generic(problem, enqueue_condition=None) :
    """
    Solves the problem, calling propagate with the specified enqueue
    condition (a function). If enqueue_condition is None, uses DFS only.
    Same return type as solve_constraint_dfs.
    """
    if enqueue_condition is None:
        return solve_constraint_dfs(problem)
    else:
        problem_copy = problem.copy()
        
        extensions = 0
        queue = [problem_copy]
        # #performs dfs on each node
        #while len(queue)>0:
        while len(queue) >0:
            next_problem = queue.pop(0)
            
            extensions += 1
            if has_empty_domains(next_problem):
                continue
            
            if check_all_constraints(next_problem) and len(next_problem.unassigned_vars) == 0:
                return(next_problem.assignments, extensions)
            
            if len(next_problem.unassigned_vars) == 0:
                #if there are no more variables to assign, just want to keep iterating through queue until find a path that satisfies
                continue
            
            #extends the queue by adding the previous problem + the next unassigned variable and the possible assignments of that unassigned variable
            next_unassigned_var = next_problem.pop_next_unassigned_var()
            unassigned_domain = next_problem.get_domain(next_unassigned_var)
            
            new_problems = []
            for assig in unassigned_domain:
                problem_to_add_to_queue = next_problem.copy()
                if check_all_constraints(problem_to_add_to_queue):
                    
                    problem_to_add_to_queue.set_assignment(next_unassigned_var, assig)
                   
                
                    propagate(enqueue_condition, problem_to_add_to_queue, [next_unassigned_var])
                    new_problems.append(problem_to_add_to_queue)
            
            queue = new_problems + queue
            
            
        return (None, extensions)

# QUESTION 5: How many extensions does it take to solve the Pokemon problem
#    with forward checking and propagation through singleton domains? (Don't
#    use domain reduction before solving it.)

ANSWER_5 = solve_constraint_generic(get_pokemon_problem(), condition_singleton )[1]


#### Part 6: Defining Custom Constraints #######################################

def constraint_adjacent(m, n) :
    """Returns True if m and n are adjacent, otherwise False.
    Assume m and n are ints."""
    if n == (m-1) or n== (m+1):
        return True
    return False

def constraint_not_adjacent(m, n) :
    """Returns True if m and n are NOT adjacent, otherwise False.
    Assume m and n are ints."""
    if n == (m-1) or n== (m+1):
        return False
    return True

def all_different(variables) :
    """Returns a list of constraints, with one difference constraint between
    each pair of variables."""
    pairs_of_variables = []
    var_c = variables.copy()
    #generates all the possible pairs of variables
    while len(var_c) >0:
        first_var = var_c.pop(0)
        for var in var_c:
            pairs_of_variables.append([first_var, var])
        
    #iterates through pairs of variables and set constraints for them
    constraints = []
    for pair in pairs_of_variables:
        
        new_constraint = Constraint(pair[0], pair[1], constraint_different)
        constraints.append(new_constraint)
    return constraints


#### SURVEY ####################################################################

NAME = 'Athena Nguyen'
COLLABORATORS = 'Somaia Saba, Haldrian Iriawan'
HOW_MANY_HOURS_THIS_LAB_TOOK = '15'
WHAT_I_FOUND_INTERESTING = None
WHAT_I_FOUND_BORING = 'Nothing'
SUGGESTIONS = None
