# MIT 6.034 Lab 6: k-Nearest Neighbors and Identification Trees
# Written by 6.034 Staff

from api import *
from data import *
import math
log2 = lambda x: math.log(x, 2)
INF = float('inf')


################################################################################
############################# IDENTIFICATION TREES #############################
################################################################################


#### Part 1A: Classifying points ###############################################

def id_tree_classify_point(point, id_tree):
    """Uses the input ID tree (an IdentificationTreeNode) to classify the point.
    Returns the point's classification."""
    if id_tree.is_leaf():
        return id_tree.get_node_classification()
    return id_tree_classify_point(point, id_tree.apply_classifier(point))


#### Part 1B: Splitting data with a classifier #################################

def split_on_classifier(data, classifier):
    """Given a set of data (as a list of points) and a Classifier object, uses
    the classifier to partition the data.  Returns a dict mapping each feature
    values to a list of points that have that value."""
    split_on_classifier_dict= {}
    for point in data:
        point_class = classifier.classify(point)
        if point_class not in split_on_classifier_dict.keys():
            split_on_classifier_dict[point_class] = [point]
        else:
            split_on_classifier_dict[point_class].append(point)   
    return split_on_classifier_dict


#### Part 1C: Calculating disorder #############################################

def branch_disorder(data, target_classifier):
    """Given a list of points representing a single branch and a Classifier
    for determining the true classification of each point, computes and returns
    the disorder of the branch."""
    classified_data = split_on_classifier(data, target_classifier)
    return sum([-(len(classified_data[classification])/len(data))*math.log(len(classified_data[classification])/len(data),2) for classification in classified_data.keys()])

def average_test_disorder(data, test_classifier, target_classifier):
    """Given a list of points, a feature-test Classifier, and a Classifier
    for determining the true classification of each point, computes and returns
    the disorder of the feature-test stump."""
    test = split_on_classifier(data, test_classifier)
    return sum([len(test[branch])/len(data)*  branch_disorder(test[branch], target_classifier) for branch in test.keys()])

## To use your functions to solve part A2 of the "Identification of Trees"
## problem from 2014 Q2, uncomment the lines below and run lab6.py:

# for classifier in tree_classifiers:
#     print(classifier.name, average_test_disorder(tree_data, classifier, feature_test("tree_type")))


#### Part 1D: Constructing an ID tree ##########################################

def find_best_classifier(data, possible_classifiers, target_classifier):
    """Given a list of points, a list of possible Classifiers to use as tests,
    and a Classifier for determining the true classification of each point,
    finds and returns the classifier with the lowest disorder.  Breaks ties by
    preferring classifiers that appear earlier in the list.  If the best
    classifier has only one branch, raises NoGoodClassifiersError."""
    #initiatie score (always want to find something lower) and best classifer 
    best_score = INF
    best_classifier = None

    #iterate through classifiers to find disorder
    for classifier in possible_classifiers:
        score = average_test_disorder(data, classifier, target_classifier)
        #if find classifier with lower score, replace best score and classifeir
        if score < best_score:
            best_score = score
            best_classifier = classifier

    if best_classifier is None: #no good classifiers
        raise NoGoodClassifiersError 
    elif len(split_on_classifier(data, best_classifier).keys()) ==1 or len(split_on_classifier(data, best_classifier).keys()) ==0:
        raise NoGoodClassifiersError
    else:
        return best_classifier


## To find the best classifier from 2014 Q2, Part A, uncomment:
# print(find_best_classifier(tree_data, tree_classifiers, feature_test("tree_type")))

def construct_greedy_id_tree(data, possible_classifiers, target_classifier, id_tree_node=None):
    """Given a list of points, a list of possible Classifiers to use as tests,
    a Classifier for determining the true classification of each point, and
    optionally a partially completed ID tree, returns a completed ID tree by
    adding classifiers and classifications until either perfect classification
    has been achieved, or there are no good classifiers left."""
    
    #keep picking test with lowest disorder until all training data are classified or there are no more tests
    #must recalculate disorders of all the tests w/ every time we pick a test
    # return construct_greedy_id_tree(data, possible_classifiers, target_classifier, id_tree_node=None)
    
    if id_tree_node is None:
        id_tree_node = IdentificationTreeNode(target_classifier)
    #base case
    if branch_disorder(data, target_classifier) == 0:
        id_tree_node.set_node_classification(target_classifier.classify(data[0]))
        return id_tree_node

    try:
        
        best_classifier = find_best_classifier(data, possible_classifiers, target_classifier)
        split_data = split_on_classifier(data, best_classifier)
        id_tree_node.set_classifier_and_expand(best_classifier,split_data.keys())
        branches = id_tree_node.get_branches()
        for branch in branches.keys():
            construct_greedy_id_tree(split_data[branch], possible_classifiers, target_classifier, branches[branch])
        return id_tree_node
    except NoGoodClassifiersError:
        return id_tree_node
    


## To construct an ID tree for 2014 Q2, Part A:
# print(construct_greedy_id_tree(tree_data, tree_classifiers, feature_test("tree_type")))

## To use your ID tree to identify a mystery tree (2014 Q2, Part A4):
# tree_tree = construct_greedy_id_tree(tree_data, tree_classifiers, feature_test("tree_type"))
# print(id_tree_classify_point(tree_test_point, tree_tree))

## To construct an ID tree for 2012 Q2 (Angels) or 2013 Q3 (numeric ID trees):
# print(construct_greedy_id_tree(angel_data, angel_classifiers, feature_test("Classification")))
# print(construct_greedy_id_tree(numeric_data, numeric_classifiers, feature_test("class")))


#### Part 1E: Multiple choice ##################################################

ANSWER_1 = 'bark_texture'
ANSWER_2 = 'leaf_shape'
ANSWER_3 = 'orange_foliage'

ANSWER_4 = [2,3]
ANSWER_5 = [3]
ANSWER_6 = [2]
ANSWER_7 = 2

ANSWER_8 = 'No'
ANSWER_9 = 'No'


#### OPTIONAL: Construct an ID tree with medical data ##########################

## Set this to True if you'd like to do this part of the lab
DO_OPTIONAL_SECTION = False

if DO_OPTIONAL_SECTION:
    from parse import *
    medical_id_tree = construct_greedy_id_tree(heart_training_data, heart_classifiers, heart_target_classifier_discrete)


################################################################################
############################# k-NEAREST NEIGHBORS ##############################
################################################################################

#### Part 2A: Drawing Boundaries ###############################################

BOUNDARY_ANS_1 = 3
BOUNDARY_ANS_2 = 4

BOUNDARY_ANS_3 = 1
BOUNDARY_ANS_4 = 2

BOUNDARY_ANS_5 = 2
BOUNDARY_ANS_6 = 4
BOUNDARY_ANS_7 = 1
BOUNDARY_ANS_8 = 4
BOUNDARY_ANS_9 = 4

BOUNDARY_ANS_10 = 4
BOUNDARY_ANS_11 = 2
BOUNDARY_ANS_12 = 1
BOUNDARY_ANS_13 = 4
BOUNDARY_ANS_14 = 4


#### Part 2B: Distance metrics #################################################

def dot_product(u, v):
    """Computes dot product of two vectors u and v, each represented as a tuple
    or list of coordinates.  Assume the two vectors are the same length."""
    return sum([u[i] * v[i] for i in range(len(u))])

def norm(v):
    "Computes length of a vector v, represented as a tuple or list of coords."
    return (sum([(v[i])**2 for i in range(len(v))]))**(1/2)

def euclidean_distance(point1, point2):
    "Given two Points, computes and returns the Euclidean distance between them."
    return (sum([(point1.coords[i] -point2.coords[i])**2 for i in range(len(point1.coords))]))**(1/2)

def manhattan_distance(point1, point2):
    "Given two Points, computes and returns the Manhattan distance between them."
    return sum([abs(point1.coords[i] -point2.coords[i]) for i in range(len(point1.coords))])

def hamming_distance(point1, point2):
    "Given two Points, computes and returns the Hamming distance between them."
    return sum([1 for i in range(len(point1.coords)) if point1.coords[i] != point2.coords[i]])

def cosine_distance(point1, point2):
    """Given two Points, computes and returns the cosine distance between them,
    where cosine distance is defined as 1-cos(angle_between(point1, point2))."""
    return 1-(dot_product(point1.coords, point2.coords)/(norm(point1.coords)*norm(point2.coords)))


#### Part 2C: Classifying points ###############################################

def get_k_closest_points(point, data, k, distance_metric):
    """Given a test point, a list of points (the data), an int 0 < k <= len(data),
    and a distance metric (a function), returns a list containing the k points
    from the data that are closest to the test point, according to the distance
    metric.  Breaks ties lexicographically by coordinates."""
    lexo_data = sorted(data, key = lambda subpoint: subpoint.coords)
    sorted_data = sorted(lexo_data, key=lambda index: distance_metric(point, index))
    return [sorted_data[i] for i in range(k)]

def knn_classify_point(point, data, k, distance_metric):
    """Given a test point, a list of points (the data), an int 0 < k <= len(data),
    and a distance metric (a function), returns the classification of the test
    point based on its k nearest neighbors, as determined by the distance metric.
    Assumes there are no ties."""
    #sorts the data lexographically by their coordinates
    lexo_data = sorted(data, key = lambda subpoint: subpoint.coords)
    #sorts by distance
    sorted_data = sorted(lexo_data, key=lambda index: distance_metric(point, index))
    k_points_classification = [sorted_data[i].classification for i in range(k)]
    return max(k_points_classification,key=k_points_classification.count)
    

## To run your classify function on the k-nearest neighbors problem from 2014 Q2
## part B2, uncomment the line below and try different values of k:
# print(knn_classify_point(knn_tree_test_point, knn_tree_data, 1, euclidean_distance))


#### Part 2C: Choosing k #######################################################

def cross_validate(data, k, distance_metric):
    """Given a list of points (the data), an int 0 < k <= len(data), and a
    distance metric (a function), performs leave-one-out cross-validation.
    Return the fraction of points classified correctly, as a float."""
    
    correct = 0    
    for i in range(len(data)):
        data_copy = data.copy()
        test_point = data_copy[i]
        data_copy.remove(test_point)
        
        classified_point = knn_classify_point(test_point, data_copy, k, distance_metric)
        
        if classified_point == test_point.classification:
            
            
            correct +=1 
        
    return float(correct/len(data))
       
    
    

def find_best_k_and_metric(data):
    """Given a list of points (the data), uses leave-one-out cross-validation to
    determine the best value of k and distance_metric, choosing from among the
    four distance metrics defined above.  Returns a tuple (k, distance_metric),
    where k is an int and distance_metric is a function."""
   #find best value of k 
    distance_metrics = [euclidean_distance, manhattan_distance, hamming_distance, cosine_distance]
    metrics_k = []
    for metric in distance_metrics:
        k = 1
        while cross_validate(data, k, metric) <= cross_validate(data, k+1,metric): 
            k +=1
        metrics_k.append((k,metric))
    best_k = 0
    for m in metrics_k:
        if m[0] > best_k:
            best_k = m[0]
            best_metric = m
    return best_metric
    
## To find the best k and distance metric for 2014 Q2, part B, uncomment:
# print(find_best_k_and_metric(knn_tree_data))


#### Part 2E: More multiple choice #############################################

kNN_ANSWER_1 = 'Overfitting'
kNN_ANSWER_2 = 'Underfitting'
kNN_ANSWER_3 = 4

kNN_ANSWER_4 = 4
kNN_ANSWER_5 = 1
kNN_ANSWER_6 = 3
kNN_ANSWER_7 = 3


#### SURVEY ####################################################################

NAME = 'Athena Nguyen'
COLLABORATORS = 'Somaia Saba'
HOW_MANY_HOURS_THIS_LAB_TOOK = None
WHAT_I_FOUND_INTERESTING = None
WHAT_I_FOUND_BORING = None
SUGGESTIONS = None
