# MIT 6.034 Lab 8: Support Vector Machines
# Written by 6.034 staff

from svm_data import *
from functools import reduce
# import matplotlib

#### Part 1: Vector Math #######################################################

def dot_product(u, v):
    """Computes the dot product of two vectors u and v, each represented 
    as a tuple or list of coordinates. Assume the two vectors are the
    same length."""
    return sum([u[i]*v[i] for i in range(len(u))])      

def norm(v):
    """Computes the norm (length) of a vector v, represented 
    as a tuple or list of coords."""
    return (sum([v[i]**2 for i in range(len(v))]))**(1/2)

#### Part 2: Using the SVM Boundary Equations ##################################

def positiveness(svm, point):
    """Computes the expression (w dot x + b) for the given Point x."""
    return dot_product(svm.w, point.coords) +svm.b
    

def classify(svm, point):
    """Uses the given SVM to classify a Point. Assume that the point's true
    classification is unknown.
    Returns +1 or -1, or 0 if point is on boundary."""
    if positiveness(svm, point) > 0:
        return 1
    elif positiveness(svm, point) < 0:
        return -1
    else:
        return 0

def margin_width(svm):
    """Calculate margin width based on the current boundary."""
    return 2/norm(svm.w)

def check_gutter_constraint(svm):
    """Returns the set of training points that violate one or both conditions:
        * gutter constraint (positiveness == classification, for support vectors)
        * training points must not be between the gutters
    Assumes that the SVM has support vectors assigned."""
    
    training_violations = set()
   
    for vector in svm.support_vectors:
        for point in svm.training_points:
            
            if -1 < positiveness(svm, point) < 1 :
                training_violations.add(point)
            if vector.classification != positiveness(svm, vector):
                training_violations.add(vector)
            
    return training_violations


#### Part 3: Supportiveness ####################################################

def check_alpha_signs(svm):
    """Returns the set of training points that violate either condition:
        * all non-support-vector training points have alpha = 0
        * all support vectors have alpha > 0
    Assumes that the SVM has support vectors assigned, and that all training
    points have alpha values assigned."""
    training_violations = set()
    for point in svm.training_points:
        if point not in svm.support_vectors:
            if point.alpha != 0:
                training_violations.add(point)
    for vector in svm.support_vectors:
        if vector.alpha<=0:
            training_violations.add(vector)
    return training_violations

def check_alpha_equations(svm):
    """Returns True if both Lagrange-multiplier equations are satisfied,
    otherwise False. Assumes that the SVM has support vectors assigned, and
    that all training points have alpha values assigned."""
    eqn_4 = 0
    eqn_5 = [0,0]
    
    for point in svm.training_points:   
        eqn_4 += point.classification * point.alpha
        eqn_5 = vector_add(eqn_5, scalar_mult(point.alpha * point.classification, point) )
    return eqn_5 == svm.w and eqn_4 ==0
    
        


#### Part 4: Evaluating Accuracy ###############################################

def misclassified_training_points(svm):
    """Returns the set of training points that are classified incorrectly
    using the current decision boundary."""
    
    incorrect_training_points = set()
    for point in svm.training_points:
        if classify(svm, point) != point.classification:
            incorrect_training_points.add(point)
    return incorrect_training_points


#### Part 5: Training an SVM ###################################################

def update_svm_from_alphas(svm):
    """Given an SVM with training data and alpha values, use alpha values to
    update the SVM's support vectors, w, and b. Return the updated SVM."""
    support_vectors = [point for point in svm.training_points if point.alpha > 0]
    eqn_5 = [0,0]
    for point in svm.training_points:
        eqn_5 = vector_add(eqn_5, scalar_mult(point.alpha * point.classification, point) )
    svm.support_vectors = support_vectors
    
    svm.w = eqn_5
    pos_b = [-dot_product(svm.w, vector) for vector in support_vectors if vector.classification >0]
    neg_b = [-dot_product(svm.w, vector) for vector in support_vectors if vector.classification <0]

    svm.b = (max(pos_b)+min(neg_b))/2
    
    return svm


#### Part 6: Multiple Choice ###################################################

ANSWER_1 = 11
ANSWER_2 = 6
ANSWER_3 = 3
ANSWER_4 = 2

ANSWER_5 = ['A', 'D']
ANSWER_6 = ['A','B','D']
ANSWER_7 = ['A','B','D']
ANSWER_8 = []
ANSWER_9 = ['A','B','D']
ANSWER_10 =['A','B','D']

ANSWER_11 = False
ANSWER_12 = True
ANSWER_13 = False
ANSWER_14 = False
ANSWER_15 = False
ANSWER_16 = True

ANSWER_17 = [1,3,6,8]
ANSWER_18 = [1,2,4,5,6,7,8]
ANSWER_19 = [1,2,4,5,6,7,8]

ANSWER_20 = 6


#### SURVEY ####################################################################

NAME = 'Athena Nguyen'
COLLABORATORS = 'Somaia Saba, Ryan Mansilla, Leilani Trautman'
HOW_MANY_HOURS_THIS_LAB_TOOK = '5'
WHAT_I_FOUND_INTERESTING = None
WHAT_I_FOUND_BORING = None
SUGGESTIONS = None
