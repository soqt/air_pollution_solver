# Astar.py, April 2017 
# Based on ItrDFS.py, Ver 0.3, April 11, 2017.

''' 
Xuefei Han
UWNetID: xuefei94
CSE 415, Spring 2017, University of Washington
Instructor:  S. Tanimoto.
Assignment 3 Part II-3.
4/20/2017
'''

# A* Search of a problem space.
# The Problem should be given in a separate Python
# file using the "QUIET" file format.
# See the TowerOfHanoi.py example file for details.
# Examples of Usage:
# python3 AStar.py EightPuzzleWithHeuristics h_manhattan

import sys
from queue import PriorityQueue

# DO NOT CHANGE THIS SECTION 
if sys.argv==[''] or len(sys.argv)<2:
    import AirPollutionSolverWithHeuristics as Problem
    heuristics = lambda s: Problem.HEURISTICS['h1'](s)
    # import TowerOfHanoi as Problem
    # heuristics = lambda s: Problem.HEURISTICS['h_0'](s)
    
else:
    import importlib
    Problem = importlib.import_module(sys.argv[1])
    heuristics = lambda s: Problem.HEURISTICS[sys.argv[2]](s)
    



print("\nWelcome to AStar")
COUNT = None
BACKLINKS = {}

# DO NOT CHANGE THIS SECTION
def runAStar():
    #initial_state = Problem.CREATE_INITIAL_STATE(keyVal)
    initial_state = Problem.CREATE_INITIAL_STATE()
    print("Initial State:")
    print(initial_state)
    global COUNT, BACKLINKS
    COUNT = 0
    BACKLINKS = {}
    path, name = AStar(initial_state)
    print(str(COUNT)+" states examined.")
    return path, name

# A star search algorithm
# TODO: finish A star implementation
def AStar(initial_state):
    global COUNT, BACKLINKS
    # TODO: initialze and put first state into 
    # priority queue with respective priority
    # add any auxiliary data structures as needed
    OPEN = PriorityQueue()
    CLOSED = PriorityQueue()

    state_string = initial_state.__str__() 
    STRING_STATE = {state_string:initial_state} # create a hashtable to store (state string: state)

    GVALUE = {state_string: 0}
    FVALUE = {state_string: h(initial_state)}

    OPEN.put((FVALUE[state_string],state_string)) # put tuple (f value, sate string) into PriorityQueue
    BACKLINKS[initial_state] = -1

    while not OPEN.empty():
    # while COUNT < 100:
        S_pair = OPEN.get()
        while occurs_in(S_pair, CLOSED):
            S_pair = OPEN.get()
        CLOSED.put(S_pair)

        S_string = S_pair[1]
        S = STRING_STATE[S_string]

        # DO NOT CHANGE THIS SECTION: begining 
        if Problem.GOAL_TEST(S):
            print(Problem.GOAL_MESSAGE_FUNCTION(S))
            path = backtrace(S)
            return path, Problem.PROBLEM_NAME
        # DO NOT CHANGE THIS SECTION: end

        # TODO: finish A* implementation
        COUNT += 1
        # if (COUNT % 32)==0:
        #     print(".",end="")
        #     if (COUNT % 128)==0:
        #         print("COUNT = "+str(COUNT))
        #         print("len(OPEN)="+str(len(OPEN)))
        #         print("len(CLOSED)="+str(len(CLOSED)))

        for op in Problem.OPERATORS:
            print("Trying operator: "+op.name)
            if op.precond(S):
                new_state = op.state_transf(S)
                new_string = new_state.__str__()
                STRING_STATE[new_string] = new_state
                if (new_string in FVALUE):
                    old_f = FVALUE[new_string]
                else:
                    old_f = ''
                if (not occurs_in((old_f,new_string),OPEN)) and (not occurs_in((old_f,new_string),CLOSED)):
                    GVALUE[new_string] = GVALUE[S_string] + 1
                    FVALUE[new_string] = GVALUE[new_string] + h(new_state)

                    BACKLINKS[new_state] = S

                    OPEN.put((FVALUE[new_string],new_string))

                else:
                    old_parent = BACKLINKS[new_state]
                    old_parent_string = old_parent.__str__()
                    if (old_parent != -1):
                        temp = FVALUE[new_string] - GVALUE[old_parent_string] - 1 + GVALUE[S_string] + 1
                    else:
                        temp = FVALUE[new_string]

                    if temp < FVALUE[new_string]:
                        old_f = FVALUE[new_string]

                        GVALUE[new_string] = GVALUE[new_string] - FVALUE[new_string] + temp
                        FVALUE[new_string] = temp
                        BACKLINKS[new_state] = S

                        old_key = (old_f,new_string)
                        if occurs_in(old_key,OPEN):
                            OPEN = remove(old_key,OPEN)
                        if occurs_in(old_key,CLOSED):
                            CLOSED = remove(old_key,CLOSED)

                        OPEN.put((FVALUE[new_string],new_string))
                print(new_state)

def remove(key,pq):
    'remove the key from PriorityQueue:pq'
    templst = []
    elt = pq.get()
    while (elt != key):
        templst.append(elt)
        elt = pq.get()
    for i in templst:
        pq.put(i)
    return pq

def occurs_in(pair, pq):
    'return True if pair in PriorityQueue:pq'
    with pq.mutex:
        return pair in pq.queue

def h(s):
    'heuristics function'
    return heuristics(s)

# DO NOT CHANGE
def backtrace(S):
    global BACKLINKS
    path = []
    while not S == -1:
        path.append(S)
        S = BACKLINKS[S]
    path.reverse()
    print("Solution path: ")
    for s in path:
        print(s)
    print("\nPath length = "+str(len(path)-1))
    return path    

if __name__=='__main__':
    path, name = runAStar()
