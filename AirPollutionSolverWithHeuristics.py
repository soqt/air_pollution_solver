# Group member: Yumeng Wang, Xuefei Han, Tianjing Cai
# CSE 415 sp17

#<METADATA>
from math import sqrt

QUIET_VERSION = "0.1"
PROBLEM_NAME = "Air pollution solver with Heuristics"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['Yumeng Wang', 'Xuefei Han', 'Tianjing Cai']
PROBLEM_CREATION_DATE = "26-APR-2017"
PROBLEM_DESC=\
'''This formulation of the Air pollution solver uses generic
Python 3 constructs and has been tested with Python 3.6.
It is designed to work according to the QUIET tools interface, Version 0.1.
'''
#</METADATA>



def can_move(s, From, To):
  '''Tests whether it's legal to move to next state'''
  try:
    if s.d[From] == 400 or abs(s.d[To] - s.d[From]) > 30: return False
    '''Find combination of s.d[To]'''
  except (Exception) as e:
   print(e)

def move(s,From, To):
  '''Assuming it's legal to make the move, this computes
     the new state resulting from moving a tile'''

  return # return new state

def goal_test(s):
  '''Test for a goal state.'''
  return s.d == GOAL_STATE

def goal_message(s):
  return "Problem solved"

class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)

#<STATE>#
class State():
  def __init__(self, d):
    self.d = d


  def __str__(self):
    # Produces a textual description of a state.
    d = self.d
    txt = ''
    return txt

  def __eq__(self, s2):
    if not (type(self)==type(s2)): return False
    d1 = self.d; d2 = s2.d
    return d1 == d2

  def __hash__(self):
    return (str(self)).__hash__()

  def __copy__(self):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
    news = State([n for n in self.d])
    return news

  def __lt__(self, other):
     return  self.d < other.d
#</STATE>

#<INITIAL_STATE>
INITIAL_STATE = {'factory': 35, "emission": 400, "economy": 10000, "growth-rate": 7}

POLLUTANT_RESOURCE = {'工厂1': 15000, '工厂2': 12000, '工厂3': 13000, 'vehicle': 1000, 'household': 200,
                      'temple': 3000, 'other': 200}
CREATE_INITIAL_STATE = lambda: State(INITIAL_STATE)
#</INITIAL_STATE>

#<GOAL_TEST>
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_STATE>
GOAL_STATE = []
#<GOAL_STATE>

#<OPERATORS>
combinations = [(p, q) for p in range(400) for q in range(400)]
OPERATORS = [Operator("Change AOI(total emission) from "+ str(p) + " to " + str(q),
                      lambda s, p1=p,q1=q: can_move(s, p1,q1),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s, p1=p, q1=q: move(s, p1, q1))
             for (p, q) in combinations]
#</OPERATORS>

#<GOAL_MESSAGE_FUNCTION>
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

#<HEURISTICS>
def h_euclidean(s):
    sum = 0
    current_position = 0
    for i in s.d:
        final_position = GOAL_STATE.index(i)
        sum += sqrt(((current_position % 3) - (final_position % 3))**2
                     + (int(current_position / 3) - int(final_position / 3))**2)
        current_position += 1
    return sum

def h_hamming(s):
    sum = 0
    state = s.d
    for i in state:
        index = state.index(i)
        if not GOAL_STATE[index] == i:
            sum += 1
    return sum

def h_manhattan(s):
    sum = 0
    state = s.d
    for i in state:
        current_index = state.index(i)
        goal_index = GOAL_STATE.index(i)
        row_d = abs(goal_index % 3 - current_index % 3)
        col_d = abs(int(goal_index/3) - int(current_index/3))
        sum += row_d + col_d
    return sum

def h_custom(s):
    return 2 * h_manhattan(s) + 2* h_euclidean(s) + h_hamming(s)


HEURISTICS = {'h_euclidean': h_euclidean, 'h_hamming': h_hamming, 'h_manhattan' : h_manhattan, 'h_custom': h_custom}
#</HEURISTICS>
