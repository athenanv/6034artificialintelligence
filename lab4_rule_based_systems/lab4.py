# MIT 6.034 Lab 4: Rule-Based Systems
# Written by 6.034 staff

from production import IF, AND, OR, NOT, THEN, DELETE, forward_chain, pretty_goal_tree
from data import *
import pprint

pp = pprint.PrettyPrinter(indent=1)
pprint = pp.pprint

#### Part 1: Multiple Choice #########################################

ANSWER_1 = '2' #consequent: In forward chaining, after all the variables in a rule have been bound, 
                #which part of the rule may appear as a new assertion in the data?

ANSWER_2 = '4' #neither In backward chaining, after all the variables in a 
                #rule have been bound, which part of the rule may appear as a new assertion in the data

ANSWER_3 = '2' #why is this just 2? Why not 1 and 3? 

ANSWER_4 = '0'

ANSWER_5 = '3'

ANSWER_6 = '1'

ANSWER_7 = '0' #no answer given?

#### Part 2: Transitive Rule #########################################

# Fill this in with your rule 
transitive_rule = IF( AND('(?x) beats (?y)',
                          '(?y) beats (?z)'), 
                     THEN( '(?x) beats (?z)') ) #'a beats b', 'b beats c', 'a beats c'

# You can test your rule by uncommenting these pretty print statements
#  and observing the results printed to your screen after executing lab1.py
# pprint(forward_chain([transitive_rule], abc_data))
# pprint(forward_chain([transitive_rule], poker_data))
# pprint(forward_chain([transitive_rule], minecraft_data))


#### Part 3: Family Relations #########################################

# Define your rules here. We've given you an example rule whose lead you can follow:
# self_rule = IF(("person (?x)"), THEN ("self (?x) (?x)"))


# sibling_rule = IF( AND( "parent (?x) (?y)" , "parent (?x) (?z)", NOT( "self (?y) (?z)")), THEN( "sibling (?y) (?z)", "sibling (?z) (?y)" ))
# child_rule = IF( ("parent (?x) (?y)"), THEN( "child (?y) (?x)"))
     
# cousin_rule = IF( AND("child (?x) (?y)", "child (?w) (?z)", "sibling (?y) (?z)", NOT("self (?y) (?z)"), NOT("self (?y) (?w)"), NOT("self (?w) ('?z')"), NOT("sibling (?w) (?x)"), NOT("sibling (?x) (?w)")),THEN("cousin (?x) (?w)", "cousin (?w) (?x)"))

# grandparent_rule = IF( AND( "parent (?x) (?y)", "parent (?z) (?x)" , NOT( "self (?y) (?z)")),THEN( "grandparent (?z) (?y)" ))
# grandchild_rule = IF( AND( "parent (?x) (?y)","parent (?z) (?x)", NOT( "self (?y) (?z)") ), THEN( "grandchild (?y) (?z)" ))




# # Add your rules to this list:
# family_rules = [child_rule, self_rule, sibling_rule, cousin_rule, grandparent_rule, grandchild_rule ]

identity_rule = IF(("person (?x)"), THEN ("identity (?x) (?x)")) #to avoid repeats of same person


sibling_rule = IF( AND( "parent (?x) (?y)" , "parent (?x) (?z)", NOT( "identity (?y) (?z)")), THEN( "sibling (?y) (?z)", "sibling (?z) (?y)" ))
child_rule = IF( ("parent (?x) (?y)"), THEN( "child (?y) (?x)"))
     
cousin_rule = IF( AND("child (?x) (?y)", "child (?w) (?z)", "sibling (?y) (?z)", NOT("identity (?y) (?z)"), NOT("identity (?y) (?w)"), NOT("self (?w) ('?z')"), NOT("sibling (?w) (?x)"), NOT("sibling (?x) (?w)")),THEN("cousin (?x) (?w)", "cousin (?w) (?x)"))

grandparent_rule = IF( AND( "parent (?x) (?y)", "parent (?z) (?x)" , NOT( "identity (?y) (?z)")),THEN( "grandparent (?z) (?y)" ))
grandchild_rule = IF( AND( "parent (?x) (?y)","parent (?z) (?x)", NOT( "identity (?y) (?z)") ), THEN( "grandchild (?y) (?z)" ))




# Add your rules to this list:
family_rules = [child_rule, identity_rule, sibling_rule, cousin_rule, grandparent_rule, grandchild_rule ]



# Uncomment this to test your data on the Simpsons family:
# pprint(forward_chain(family_rules, simpsons_data, verbose=False))

# These smaller datasets might be helpful for debugging:
#pprint(forward_chain(family_rules, sibling_test_data, verbose=True))
# pprint(forward_chain(family_rules, grandparent_test_data, verbose=True))

# The following should generate 14 cousin relationships, representing 7 pairs
# of people who are cousins:
harry_potter_family_cousins = [
    relation for relation in
    forward_chain(family_rules, harry_potter_family_data, verbose=False)
    if "cousin" in relation ]

# To see if you found them all, uncomment this line:
# pprint(harry_potter_family_cousins)


#### Part 4: Backward Chaining #########################################

# Import additional methods for backchaining
from production import PASS, FAIL, match, populate, simplify, variables

def backchain_to_goal_tree(rules, hypothesis):
    """
    Takes a hypothesis (string) and a list of rules (list
    of IF objects), returning an AND/OR tree representing the
    backchain of possible statements we may need to test
    to determine if this hypothesis is reachable or not.

    This method should return an AND/OR tree, that is, an
    AND or OR object, whose constituents are the subgoals that
    need to be tested. The leaves of this tree should be strings
    (possibly with unbound variables), *not* AND or OR objects.
    Make sure to use simplify(...) to flatten trees where appropriate.
    """
    
    
    #check to see if hypothesis is in list of assertions, if so we are done!
    #find all the fules w/ consequents that match the hypothesis
    #build the tree of bound antecedents
    #depth first serch with backtracking if we get stuck
    #return AND/OR tree
   
    backchain_tree = []
    if hypothesis == " ":
        None
    else:
        for rule in rules:
            bindings = match(rule.consequent(), hypothesis)
            if bindings is None:
                continue
            elif len(bindings) == 0:
                new_matches = []
                for i in rule.antecedent():
                    new_matches.append(backchain_to_goal_tree(rules, i))
                if isinstance(rule.antecedent(), AND):
                    backchain_tree.append(AND(new_matches))
                elif isinstance(rule.antecedent(), OR):
                    backchain_tree.append(OR(new_matches))
            else:
                new_hypotheses = populate(rule.antecedent(), bindings)
                if type(new_hypotheses) is str:
                    new_hypotheses = AND(new_hypotheses)
                new_matches = []
                for hyp in new_hypotheses:
                    new_matches.append(backchain_to_goal_tree(rules, hyp))
                if isinstance(new_hypotheses, AND):
                    backchain_tree.append(AND(new_matches))
                elif isinstance(new_hypotheses, OR):
                    backchain_tree.append(OR(new_matches))
    return simplify(OR([hypothesis]+ backchain_tree))
                    
            
      
        
    

# Uncomment this to test out your backward chainer:
# pretty_goal_tree(backchain_to_goal_tree(zookeeper_rules, 'opus is a penguin'))


#### Survey #########################################

NAME = 'Athena Nguyen'
COLLABORATORS = 'Somaia Saba, Grace Chang,  Ginny Rosenberger, Vinit Kaushik'
HOW_MANY_HOURS_THIS_LAB_TOOK = '15'
WHAT_I_FOUND_INTERESTING = None
WHAT_I_FOUND_BORING = None
SUGGESTIONS = None


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

# The following lines are used in the tester. DO NOT CHANGE!
print("(Doing forward chaining. This may take a minute.)")
transitive_rule_poker = forward_chain([transitive_rule], poker_data)
transitive_rule_abc = forward_chain([transitive_rule], abc_data)
transitive_rule_minecraft = forward_chain([transitive_rule], minecraft_data)
family_rules_simpsons = forward_chain(family_rules, simpsons_data)
family_rules_harry_potter_family = forward_chain(family_rules, harry_potter_family_data)
family_rules_sibling = forward_chain(family_rules, sibling_test_data)
family_rules_grandparent = forward_chain(family_rules, grandparent_test_data)
family_rules_anonymous_family = forward_chain(family_rules, anonymous_family_test_data)
