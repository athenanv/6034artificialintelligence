# MIT 6.034 Lab 9: Boosting (Adaboost)
# Written by 6.034 staff

from math import log as ln
from utils import *


#### Part 1: Helper functions ##################################################

def initialize_weights(training_points):
    """Assigns every training point a weight equal to 1/N, where N is the number
    of training points.  Returns a dictionary mapping points to weights."""
    return {key: make_fraction(1, len(training_points)) for key in training_points}

def calculate_error_rates(point_to_weight, classifier_to_misclassified):
    """Given a dictionary mapping training points to their weights, and another
    dictionary mapping classifiers to the training points they misclassify,
    returns a dictionary mapping classifiers to their error rates."""
    error_rates = {}
    for classifier in classifier_to_misclassified.keys():
        if len(classifier_to_misclassified[classifier]) == 0:
            error_rates[classifier] = 0
        for point in classifier_to_misclassified[classifier]:
            if classifier not in error_rates.keys():
                error_rates[classifier] = point_to_weight[point]
            else:
                error_rates[classifier] += point_to_weight[point]

    return error_rates

def pick_best_classifier(classifier_to_error_rate, use_smallest_error=True):
    """Given a dictionary mapping classifiers to their error rates, returns the
    best* classifier, or raises NoGoodClassifiersError if best* classifier has
    error rate 1/2.  best* means 'smallest error rate' if use_smallest_error
    is True, otherwise 'error rate furthest from 1/2'."""
    if use_smallest_error:
        min_value = min(classifier_to_error_rate.values()) 
        best_classifier = [key for key in classifier_to_error_rate if classifier_to_error_rate[key] == min_value]
        
        if make_fraction(classifier_to_error_rate[best_classifier[0]]) == 1/2:
            raise NoGoodClassifiersError
        else:
            return best_classifier[0]
    else:
        furthest = make_fraction(abs(1/2 - classifier_to_error_rate[list(classifier_to_error_rate.keys())[0]]))
        best_classifier = list(classifier_to_error_rate.keys())[0]
        for classifier in classifier_to_error_rate.keys():
            if make_fraction(abs(1/2 -classifier_to_error_rate[classifier])) > furthest:
                furthest = make_fraction(abs(1/2 -classifier_to_error_rate[classifier]))
                best_classifier = classifier
        if classifier_to_error_rate[best_classifier] == 1/2:
            raise NoGoodClassifiersError
        else:
            return best_classifier
                
        
        

def calculate_voting_power(error_rate):
    """Given a classifier's error rate (a number), returns the voting power
    (aka alpha, or coefficient) for that classifier."""
    if error_rate <= 0:
        return INF
    elif error_rate >= 1:
        return -INF
    return 1/2 * ln((1-error_rate)/error_rate)

def get_overall_misclassifications(H, training_points, classifier_to_misclassified):
    """Given an overall classifier H, a list of all training points, and a
    dictionary mapping classifiers to the training points they misclassify,
    returns a set containing the training points that H misclassifies.
    H is represented as a list of (classifier, voting_power) tuples."""
    misclassified_points = set()

    for point in training_points:
        wrong_classifier = []
        for key in classifier_to_misclassified.keys():
            if point in classifier_to_misclassified[key]:
                wrong_classifier.append(key)
        
        voting_overall = 0
        for classifier, voting in H:
            if classifier in wrong_classifier:
                voting_overall -= voting
            if classifier not in wrong_classifier:
                voting_overall += voting
        
        if voting_overall <= 0:
            misclassified_points.add(point)
    return misclassified_points
            

def is_good_enough(H, training_points, classifier_to_misclassified, mistake_tolerance=0):
    """Given an overall classifier H, a list of all training points, a
    dictionary mapping classifiers to the training points they misclassify, and
    a mistake tolerance (the maximum number of allowed misclassifications),
    returns False if H misclassifies more points than the tolerance allows,
    otherwise True.  H is represented as a list of (classifier, voting_power)
    tuples."""
    return len(get_overall_misclassifications(H, training_points, classifier_to_misclassified)) <= mistake_tolerance

def update_weights(point_to_weight, misclassified_points, error_rate):
    """Given a dictionary mapping training points to their old weights, a list
    of training points misclassified by the current weak classifier, and the
    error rate of the current weak classifier, returns a dictionary mapping
    training points to their new weights.  This function is allowed (but not
    required) to modify the input dictionary point_to_weight."""
    
    for point in point_to_weight.keys():
        old_weight = point_to_weight[point]
        if point not in misclassified_points:
            
            if error_rate == 1:
                point_to_weight[point] = INF
            else:
                point_to_weight[point] = make_fraction((1/2)*(1/(1-error_rate))*old_weight)
        else:
            if error_rate == 0:
                point_to_weight[point] = INF
            else:
                point_to_weight[point] = make_fraction((1/2)*(1/error_rate)*old_weight)
    return point_to_weight

#### Part 2: Adaboost ##########################################################

def adaboost(training_points, classifier_to_misclassified,
             use_smallest_error=True, mistake_tolerance=0, max_rounds=INF):
    """Performs the Adaboost algorithm for up to max_rounds rounds.
    Returns the resulting overall classifier H, represented as a list of
    (classifier, voting_power) tuples."""
    
    count = 0
    #initialize weights
    point_to_weight = initialize_weights(training_points)
    H = []
    while count < max_rounds:
        count += 1
        #calculate error rate
        
        error_rates = calculate_error_rates(point_to_weight, classifier_to_misclassified)
        #pick best classifier
        try:
            best_classifier = pick_best_classifier(error_rates, use_smallest_error)
            
        except NoGoodClassifiersError:
            return H
        
        #calculate voiting power
        error_rate = error_rates[best_classifier]
        
        voting_power = calculate_voting_power(error_rate)
        #append it to the ensemble classifier
        H.append((best_classifier, voting_power))
       
        if is_good_enough(H, training_points, classifier_to_misclassified, mistake_tolerance):
            return H
        
        misclassified_points = classifier_to_misclassified[best_classifier]

        point_to_weight = update_weights(point_to_weight, misclassified_points, error_rate)
        
   
    return H


#### SURVEY ####################################################################

NAME = 'Athena Nguyen'
COLLABORATORS = None
HOW_MANY_HOURS_THIS_LAB_TOOK = None
WHAT_I_FOUND_INTERESTING = None
WHAT_I_FOUND_BORING = None
SUGGESTIONS = None
