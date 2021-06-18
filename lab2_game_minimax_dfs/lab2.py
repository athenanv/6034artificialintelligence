# MIT 6.034 Lab 2: Games
# Written by 6.034 staff

from game_api import *
from boards import *
from toytree import GAME1


INF = float('inf')

# Please see wiki lab page for full description of functions and API.

##Purpose: Play a game using minimax, alpha beta, and progressive deepening

#### Part 1: Utility Functions #################################################

def is_game_over_connectfour(board):
    """Returns True if game is over, otherwise False."""
    
    #if someone wins or board is full, return True
    chains = board.get_all_chains()
    for chain in chains:
        if len(chain) >= 4:
            return True
    #if there are open spaces in the top row, there are more moves to be made
    top_row = board.board_array[0]
    for i in top_row:
        if i is None:
            return False
   
    return True

def next_boards_connectfour(board):
    """Returns a list of ConnectFourBoard objects that could result from the
    next move, or an empty list if no moves can be made."""
    if is_game_over_connectfour(board):
        return []
    #iterate through columns and add a piece unless full
    next_moves= []
    for col in range(0,7):
        if board.is_column_full(col):
            continue
        next_moves.append(board.add_piece(col, player=None))

    return next_moves

def endgame_score_connectfour(board, is_current_player_maximizer):
    """Given an endgame board, returns 1000 if the maximizer has won,
    -1000 if the minimizer has won, or 0 in case of a tie."""
    
    if is_game_over_connectfour(board):
        filled_count = 0
        for col in range(0,7): # if all columns are full
            if board.is_column_full(col) :
                filled_count += 1
        if filled_count == 7:
            return 0
        elif is_current_player_maximizer: #if minimizer won
            return -1000
        elif not is_current_player_maximizer: #if maximizer won
            return 1000

def endgame_score_connectfour_faster(board, is_current_player_maximizer):
    """Given an endgame board, returns an endgame score with abs(score) >= 1000,
    returning larger absolute scores for winning sooner."""
    
    
    #use board.count_pieces() to tell how fast they did it
    if is_game_over_connectfour(board):
        filled_count = 0
        for col in range(0,7): # if all columns are full
            if board.is_column_full(col) :
                filled_count += 1
        if filled_count == 7:
            return 0
        
        elif is_current_player_maximizer: #if minimizer won
            return (-1000*(42-board.count_pieces())) #first is smaller than next value
        elif not is_current_player_maximizer: #if maximizer won
            return 1000*(42-board.count_pieces())
    

def heuristic_connectfour(board, is_current_player_maximizer):
    """Given a non-endgame board, returns a heuristic score with
    abs(score) < 1000, where higher numbers indicate that the board is better
    for the maximizer."""
    chains = board.get_all_chains()
    
    count_1 = 0 #counter for chains with 1
    count_2 = 0 #counter for chains with 2
    heur_1 =1
    heur_2 = 1
    
    #for loop keeps track of number of chains with 1's and 2's
    #adds to heuristic by length of chain, prioritizing those with longer chains
    #adds to the count of each chain, prioritizing those with longer chains
    for chain in chains:
        if chain[0] == 1:
            heur_1 += len(chain)
            if len(chain)!= 1:
                count_1 += len(chain)
        elif chain[0] ==2:
            heur_2 += len(chain)
            if len(chain) !=1:
                count_2 += len(chain)
                
    #establishes heuristic by adding the lens of the chains with the number of chains
    heur_1 += count_1
    heur_2 += count_2
    
    #assuming the chains with 1's in it are the maximizer and the 2's for the minimizer
    #if maximizer and doing better, than returns the positive of the maximizer's heuristic and if maximizer 
    # is doing worse, then returns negative of minimizer's score
    if is_current_player_maximizer:
        if heur_1 > heur_2:
            return heur_1
        elif heur_1 < heur_2:
            return -heur_2
        elif heur_1 == heur_2:
            return 0
    #vice versa logic of above
    elif not is_current_player_maximizer:
        if heur_2 > heur_1:
            return heur_2
        elif heur_2 < heur_1:
            return -heur_1
        elif heur_1 == heur_2:
            return 0
    
        

# Now we can create AbstractGameState objects for Connect Four, using some of
# the functions you implemented above.  You can use the following examples to
# test your dfs and minimax implementations in Part 2.

# This AbstractGameState represents a new ConnectFourBoard, before the game has started:
state_starting_connectfour = AbstractGameState(snapshot = ConnectFourBoard(),
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "NEARLY_OVER" from boards.py:
state_NEARLY_OVER = AbstractGameState(snapshot = NEARLY_OVER,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "BOARD_UHOH" from boards.py:
state_UHOH = AbstractGameState(snapshot = BOARD_UHOH,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)


#### Part 2: Searching a Game Tree #############################################

# Note: Functions in Part 2 use the AbstractGameState API, not ConnectFourBoard.

def dfs_maximizing(state) :
    """Performs depth-first search to find path with highest endgame score.
    Returns a tuple containing:
     0. the best path (a list of AbstractGameState objects),
     1. the score of the leaf node (a number), and
     2. the number of static evaluations performed (a number)"""
    #trackers for static evaluations and the score of leaf node
    stat_eval= 0
    best_num = 0
    
    
    #starts out the queue with the starting starting and children of first node
    queue= []
    next_state = state.generate_next_states()
    for e in next_state:
        queue_loop = [state]
        queue_loop.append(e)
        queue.append(queue_loop)
    
    
    #performs dfs on each node
    while len(queue)>0:
        #pops first thing off the queue and generates the next states
        front = queue.pop(0) 
        next_states = front[-1].generate_next_states() #gets the children
        
        #if at leaf node (when there are no children), we want to get 1 to static eval
        #and get the score at the leaf node
        if len(next_states)==0:
            stat_eval += 1
            score = front[-1].get_endgame_score()
            
            #if best score so far, keep that best score and make path into best path
            if score > best_num:
                
                best_num = score
                best_path = front
        else:
            #if not at leaf node, we want to add to the queue
            #each addition to the queue is a list of the path popped off before and a child of the node
            for i in next_states:
                queue_loop = front.copy()
                queue_loop.append(i)
                queue.append(queue_loop)
    
    return (best_path, best_num, stat_eval)


# look at all the scores of children and find the best one
    
    
# Uncomment the line below to try your dfs_maximizing on an
# AbstractGameState representing the games tree "GAME1" from toytree.py:
# print(dfs_maximizing(GAME1))
# pretty_print_dfs_type(dfs_maximizing(GAME1))


def minimax_endgame_search(state, maximize=True) :
    """Performs minimax search, searching all leaf nodes and statically
    evaluating all endgame scores.  Same return type as dfs_maximizing."""
    
    
    children = state.generate_next_states()
   
    if state.is_game_over() or len(children) == 0: #base case
        
        #get score based on if maximizer or minimizer
        if maximize == True:
            score = state.get_endgame_score(True)
        elif maximize==False:
            score = state.get_endgame_score(False)
        stat_eval = 1
        
        return ([state], score,stat_eval)
        
    #recursive step: look ahead at opponent's counter move
    else:
        min_num = float(INF)
        max_num = -float(INF)
        init_path = [state]
        static = 0
        if maximize == True: 
            
            for child in children:
                path = init_path.copy()
                static += minimax_endgame_search(child, maximize =False)[2] #static eval
                path = path+minimax_endgame_search(child, maximize =False)[0]
                max_values =minimax_endgame_search(child, maximize =False)[1] #keep track of scores to later evaluate max of 
                #if find better value
                if max_values > max_num:
                    max_num = max_values
                    best_path = path
                
                
            return (best_path, max_num, static)
        
        elif maximize==False : # min's turn with opposite logic of max
            
            for child in children:
                path = init_path.copy()
                static+=minimax_endgame_search(child, maximize =True)[2]
                min_values = minimax_endgame_search(child, maximize =True)[1]
                path = path+minimax_endgame_search(child, maximize =True)[0]
                if min_values < min_num:
                    min_num=min_values
                    best_path = path
                
                
            return (best_path, min_num, static)

        


# Uncomment the line below to try your minimax_endgame_search on an
# AbstractGameState representing the ConnectFourBoard "NEARLY_OVER" from boards.py:

# pretty_print_dfs_type(minimax_endgame_search(state_NEARLY_OVER))


def minimax_search(state, heuristic_fn=always_zero, depth_limit=INF, maximize=True) :
    """Performs standard minimax search. Same return type as dfs_maximizing."""
    
    children = state.generate_next_states()
   
    if state.is_game_over(): #base case
        
        if maximize == True:
            return ([state], state.get_endgame_score(True),1)
        elif maximize == False:
            return ([state], state.get_endgame_score(False),1)
        
        
    elif depth_limit ==0:
        if maximize == True:
            heur=heuristic_fn(state.get_snapshot(), True)
        elif maximize == False:
            heur =heuristic_fn(state.get_snapshot(), False)
        
        
        return ([state], heur,1)
    #recursive step: look ahead at opponent's counter move
    else:
        min_num = INF
        max_num = -INF
        #initializes a path to add
        init_path = [state]
        static = 0
        best_path = []
        #looks for static number, path, and min/max number
        for child in children:
            path = init_path.copy()
            if maximize == True:
                path = path + minimax_search(child, heuristic_fn,
                             depth_limit-1, maximize=False)[0]
                score = minimax_search(child, heuristic_fn,
                             depth_limit-1, maximize=False)[1]
                static += minimax_search(child,  heuristic_fn,
                             depth_limit-1, maximize=False)[2]
                
                if score> max_num:
                    max_num = score
                    best_path = path
            elif maximize == False:
                path = path + minimax_search(child,  heuristic_fn,
                             depth_limit-1, maximize=True)[0]
                score = minimax_search(child, heuristic_fn,
                             depth_limit-1, maximize=True)[1]
                static += minimax_search(child, heuristic_fn,
                             depth_limit-1, maximize=True)[2]
                if score< min_num:
                    min_num = score
                    best_path = path
        if maximize:
            score = max_num
            return (best_path, score, static)
        elif not maximize:
            score = min_num
            return (best_path, score, static)



# Uncomment the line below to try minimax_search with "BOARD_UHOH" and
# depth_limit=1. Try increasing the value of depth_limit to see what happens:

# pretty_print_dfs_type(minimax_search(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=1))


def minimax_search_alphabeta(state, alpha=-INF, beta=INF, heuristic_fn=always_zero,
                             depth_limit=INF, maximize=True) :
    """"Performs minimax with alpha-beta pruning. Same return type 
    as dfs_maximizing."""
    
    children = state.generate_next_states()
   
    if state.is_game_over(): #base case
        
        if maximize == True:
            return ([state], state.get_endgame_score(True),1)
        elif maximize == False:
            return ([state], state.get_endgame_score(False),1)
        
        
    elif depth_limit ==0:
        if maximize == True:
            heur=heuristic_fn(state.get_snapshot(), True)
        elif maximize == False:
            heur =heuristic_fn(state.get_snapshot(), False)
        
        
        return ([state], heur,1)
    #recursive step: look ahead at opponent's counter move
    else:
        min_num = INF
        max_num = -INF
        #initializes a path to add
        init_path = [state]
        static = 0
        best_path = []
        #looks for static number, path, and min/max number
        for child in children:
            path = init_path.copy()
            if maximize == True:
                path = path + minimax_search_alphabeta(child, alpha, beta, heuristic_fn,
                             depth_limit-1, maximize=False)[0]
                score = minimax_search_alphabeta(child, alpha, beta, heuristic_fn,
                             depth_limit-1, maximize=False)[1]
                static += minimax_search_alphabeta(child, alpha, beta, heuristic_fn,
                             depth_limit-1, maximize=False)[2]
                if score> max_num:
                    max_num = score
                    best_path = path
                #alpha beta pruning
                if max_num > alpha:
                    alpha = max_num
                elif max_num < alpha:
                    max_num = alpha
                if alpha  >= beta:
                    break
                
            elif maximize == False:
                path = path + minimax_search_alphabeta(child, alpha, beta, heuristic_fn,
                             depth_limit-1, maximize=True)[0]
                score = minimax_search_alphabeta(child, alpha, beta, heuristic_fn,
                             depth_limit-1, maximize=True)[1]
                static += minimax_search_alphabeta(child, alpha, beta, heuristic_fn,
                             depth_limit-1, maximize=True)[2]
                
                if score< min_num:
                    min_num = score
                    best_path = path
                #alpha beta pruning
                if min_num < beta:
                    beta = min_num
                elif min_num > beta:
                    min_num = beta
                if alpha >=beta:
                    break
        if maximize:
            score = max_num
            return (best_path, score, static)
        elif not maximize:
            score = min_num
            return (best_path, score, static)
        


# Uncomment the line below to try minimax_search_alphabeta with "BOARD_UHOH" and
# depth_limit=4. Compare with the number of evaluations from minimax_search for
# different values of depth_limit.

# pretty_print_dfs_type(minimax_search_alphabeta(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4))


def progressive_deepening(state, heuristic_fn=always_zero, depth_limit=INF,
                          maximize=True) :
    """Runs minimax with alpha-beta pruning. At each level, updates anytime_value
    with the tuple returned from minimax_search_alphabeta. Returns anytime_value."""
    #create an Anytime Object
    
    anytime = AnytimeValue()
    count =0
    #progresses for each depth level until it reaches the depth limit
    while count <depth_limit:
        count += 1
        
        result = minimax_search_alphabeta(state, -INF, INF, heuristic_fn, count, maximize)
        anytime.set_value(result)
    return anytime


# Uncomment the line below to try progressive_deepening with "BOARD_UHOH" and
# depth_limit=4. Compare the total number of evaluations with the number of
# evaluations from minimax_search or minimax_search_alphabeta.

# progressive_deepening(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4).pretty_print()


# Progressive deepening is NOT optional. However, you may find that 
#  the tests for progressive deepening take a long time. If you would
#  like to temporarily bypass them, set this variable False. You will,
#  of course, need to set this back to True to pass all of the local
#  and online tests.
TEST_PROGRESSIVE_DEEPENING = True
if not TEST_PROGRESSIVE_DEEPENING:
    def not_implemented(*args): raise NotImplementedError
    progressive_deepening = not_implemented


#### Part 3: Multiple Choice ###################################################

ANSWER_1 = '4'

ANSWER_2 = '1'

ANSWER_3 = '4'

ANSWER_4 = '5'


#### SURVEY ###################################################

NAME = 'Athena'
COLLABORATORS = 'Brejah Upton, Somaia Saba, Vinit Kaushik, Duaa Sharif'
HOW_MANY_HOURS_THIS_LAB_TOOK = '20'
WHAT_I_FOUND_INTERESTING = None
WHAT_I_FOUND_BORING = None
SUGGESTIONS = None
