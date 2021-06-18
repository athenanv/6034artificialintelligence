# MIT 6.034 Lab 0: Getting Started
# Written by jb16, jmn, dxh, and past 6.034 staff

from point_api import Point

#### Multiple Choice ###########################################################

# These are multiple choice questions. You answer by replacing
# the symbol 'None' with a letter (or True or False), corresponding 
# to your answer.

# True or False: Our code supports both Python 2 and Python 3
# Fill in your answer in the next line of code (True or False):
ANSWER_1 = False

# What version(s) of Python do we *recommend* for this course?
#   A. Python v2.3
#   B. Python V2.5 through v2.7
#   C. Python v3.2 or v3.3
#   D. Python v3.4 or higher
# Fill in your answer in the next line of code ("A", "B", "C", or "D"):
ANSWER_2 = "D"


################################################################################
# Note: Each function we require you to fill in has brief documentation        # 
# describing what the function should input and output. For more detailed      # 
# instructions, check out the lab 0 wiki page!                                 #
################################################################################


#### Warmup ####################################################################

def is_even(x):
    """If x is even, returns True; otherwise returns False"""
    if x %2 == 0:
        return True
    else:
        return False


def decrement(x):
    """Given a number x, returns x - 1 unless that would be less than
    zero, in which case returns 0."""
    if (x-1) < 0:
        return 0
    else:
        return x -1 

def cube(x):
    """Given a number x, returns its cube (x^3)"""
    return x**3


#### Iteration #################################################################

def is_prime(x):
    """Given a number x, returns True if it is prime; otherwise returns False"""
    newx =x
    
    if newx ==2:
        return True
    elif not isinstance(newx, int): #is it really true that decimals are not prime numbers
        return False
    elif newx == 0 or newx == 1 or newx <0 : #negative numbers are not prime
        return False
    fcount = 0
    while newx >2:    
        newx -= 1
        if abs(x)%newx== 0: #sees if it is prime
            fcount += 1
    if fcount > 0:
        return False
    return True


#says 2 is not a prime number and 0 is not prime
def primes_up_to(x):
    
    """Given a number x, returns an in-order list of all primes up to and including x"""
    primeslist = []
    i = 0
    while i<=x:
        if is_prime(i):
            primeslist.append(i)
        i+= 1
    return primeslist


#### Recursion #################################################################

def fibonacci(n):
    """Given a positive int n, uses recursion to return the nth Fibonacci number."""
    
    if n == 1 or n ==2:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def expression_depth(expr):
    """Given an expression expressed as Python lists, uses recursion to return
    the depth of the expression, where depth is defined by the maximum number of
    nested operations."""
    #haha, idk how this works
    if not isinstance(expr, list):
        return 0
    #help! I don't understand this
    else:
        return 1+ max(map(expression_depth, expr))

    #my original code that makes more sense to me but doesn't work
    # if len(expr) == 0:
    #     if expr != list:
    #         return 0
    # if len(expr) == 0:
    #     if isinstance(expr, list):
    #         print(expr == [])
    #         return 1
    # elif isinstance(expr[0], list):
        
    #     return 1+expression_depth(expr[0])+expression_depth(expr[1:])#to check if there are lists in that one
    # elif isinstance(expr[0], list) == False:
        
    #     return expression_depth(expr[1:])
    #it stops checking the rest of the list after seeing the expr[0] is a list
    
        


#### Built-in data types #######################################################


def remove_from_string(string, letters):
    """Given an original string and a string of letters, returns a new string
    which is the same as the old one except all occurrences of those letters
    have been removed from it."""
    i_word = [char for char in string] # turns each letter into an entry in a list
    r_let = [char for char in letters]
    
    for i in string:
        if i in r_let:
            
            i_word.remove(i)
            #joins the letters in the list to a word
    return ''.join(i_word)

# slight bug

def compute_string_properties(string):
    """Given a string of lowercase letters, returns a tuple containing the
    following three elements:
        0. The length of the string
        1. A list of all the characters in the string (including duplicates, if
           any), sorted in REVERSE alphabetical order
        2. The number of distinct characters in the string (hint: use a set)
    """
    
    c_list = [char for char in string]
    c_list.sort()
    c_list.reverse()
    d_char = set(string) #generates a set of each letter (doesn't repeat)
    return (len(string), c_list,len(d_char))


def tally_letters(string):
    """Given a string of lowercase letters, returns a dictionary mapping each
    letter to the number of times it occurs in the string."""
    char_dict = {}
    for char in string:
        if char not in char_dict.keys(): #adds letter if not already the key
            char_dict[char] = 1
        else:
            char_dict[char] += 1
    return char_dict



#### Functions that return functions ###########################################

def create_multiplier_function(m):
    """Given a multiplier m, returns a function that multiplies its input by m."""
    
    def multiplier(num):
        return num*m
    return multiplier

def create_length_comparer_function(check_equal):
    """Returns a function that takes as input two lists. If check_equal == True,
    this function will check if the lists are of equal lengths. If
    check_equal == False, this function will check if the lists are of different
    lengths."""
    def checker(list1,list2):
        if check_equal == True:
            return len(list1) == len(list2)
        elif check_equal == False:
            return len(list1) != len(list2)
    return checker

#Idon'tget the intuition behind this


#### Objects and APIs: Copying and modifying objects ############################

def sum_of_coordinates(point):
    """Given a 2D point (represented as a Point object), returns the sum
    of its X- and Y-coordinates."""
    x_coor=point.getX()
    
    y_coor = point.getY()
    return x_coor+y_coor

def get_neighbors(point):
    """Given a 2D point (represented as a Point object), returns a list of the
    four points that neighbor it in the four coordinate directions. Uses the
    "copy" method to avoid modifying the original point."""
    
    point_c = point.copy() 
   
    #getting point input
    x_p= point_c.getX()
    y_p = point_c.getY()
    
    #copies the point and will later modify to get neighbors
    point_c1 = point.copy()
    point_c2 = point.copy()
    point_c3 =point.copy()
    point_c4 = point.copy()
    
    #returns copied points that are modified 
    return [point_c1.setX(x_p-1), point_c2.setX(x_p+1),point_c3.setY(y_p -1),point_c4.setY(y_p+1)]   
    
    
    #return [(point_copy.setX(x_point-1), point_copy.setY(y_point)), (point_copy.setX(x_point+1), point_copy.setY(y_point)), (point_copy.setX(x_point), point_copy.setY(y_point-1)), (point_copy.setX(x_point), point_copy.setX(y_point+1)) ]
#I don't know how to call it without calling Point

#### Using the "key" argument ##################################################

def sort_points_by_Y(list_of_points):
    """Given a list of 2D points (represented as Point objects), uses "sorted"
    with the "key" argument to create and return a list of the SAME (not copied)
    points sorted in decreasing order based on their Y coordinates, without
    modifying the original list."""
    points = list_of_points.copy()
    #use lambda to sort by Y coordinates 
    sorted_points = sorted( points, key=lambda k: k.getY(),reverse =True)
    return sorted_points
        
        
#help with lambda, I have no intuition why this works
def furthest_right_point(list_of_points):
    """Given a list of 2D points (represented as Point objects), uses "max" with
    the "key" argument to return the point that is furthest to the right (that
    is, the point with the largest X coordinate)."""
    points_list=list_of_points.copy()
    #use lambda to grab the max
    max_X= max(points_list, key=lambda x: x.getX())
    return max_X


#### SURVEY ####################################################################

# How much programming experience do you have, in any language?
#     A. No experience (never programmed before this lab)
#     B. Beginner (just started learning to program, e.g. took one programming class)
#     C. Intermediate (have written programs for a couple classes/projects)
#     D. Proficient (have been programming for multiple years, or wrote programs for many classes/projects)
#     E. Expert (could teach a class on programming, either in a specific language or in general)

PROGRAMMING_EXPERIENCE = "B"


# How much experience do you have with Python?
#     A. No experience (never used Python before this lab)
#     B. Beginner (just started learning, e.g. took 6.0001)
#     C. Intermediate (have used Python in a couple classes/projects)
#     D. Proficient (have used Python for multiple years or in many classes/projects)
#     E. Expert (could teach a class on Python)

PYTHON_EXPERIENCE = "B"


# Finally, the following questions will appear at the end of every lab.
# The first three are required in order to receive full credit for your lab.

NAME = 'Athena Nguyen'
COLLABORATORS = 'None'
HOW_MANY_HOURS_THIS_LAB_TOOK = '10 hours'
SUGGESTIONS = None #optional
