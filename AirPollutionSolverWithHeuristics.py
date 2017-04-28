# Group member: Yumeng Wang, Xuefei Han, Tianjing Cai
# CSE 415 sp17

#<METADATA>
from math import sqrt

QUIET_VERSION = "0.1"
PROBLEM_NAME = "Air pollution solver with Heuristics"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['Yumeng Wang', 'Xuefei Han', 'Tianjing Cai']
PROBLEM_CREATION_DATE = "28-APR-2017"
PROBLEM_DESC=\
'''This formulation of the Air pollution solver uses generic
Python 3 constructs and has been tested with Python 3.6.
It is designed to work according to the QUIET tools interface, Version 0.1.
'''
#</METADATA>




def can_move(s,factor,unit):
  try:
    d1 = s.d
    if factor == 'population':
      ratio = d1['factory']/(d1['population'] + unit)
      if ratio < MIN_FACTORY_POPULATION_RATIO: return False
      else: return True

    if factor == 'temple':
      newTemple = d1[factor] +unit
      if newTemple < MIN_TEMPLES or newTemple > MAX_TEMPLE: return False

    if factor == 'vehicle':
      ratio = (d1[factor] + unit)/d1['population']
      if ratio < MIN_VEHICLE_POPULATION_RATIO: return False
      else:return True

    newUnits = d1[factor] + unit

    currentEcon = d1['economy']
    currentEmission = d1['emission']

    if factor=='economy' and unit < 0:
      growthRate = abs(unit/currentEcon)
      if growthRate > 0.07: return False

    newEcon = newUnits * s.getUnitEconomyGrowthFor(factor)
    newEmission = newUnits * s.getUnitEmmisionFor(factor)

    if newEmission > MAX_EMISSION: return False


    if newEmission/newEcon > 1:
      return False
    elif newEmission < currentEmission:
      return True
    elif newEcon > currentEcon:
      return True
    else:
      return False

    return False
  except (Exception) as e:
    print(e)



def move(s,factor,unit):
  news = s.__copy__()
  d1 = news.d

  d1[factor] += unit
  d1['economy'] = d1['economy'] + s.getUnitEconomyGrowthFor(factor) * unit
  d1['emission'] = d1['emission'] + s.getUnitEmmisionFor(factor) * unit


  return news



def goal_test(s):
  return s.d['emission'] == 0

def goal_message(s):
  return "The Air pollution problem is Triumphant!"

def current_list(s):
  return s.d


class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)


def h1(state):
  # print(type(state))
  now = state.d
  emi = now['emission']
  eco = now['economy']
  return emi/eco



#<STATE>#
class State():
  def __init__(self,d):
    self.d = d

  def __str__(self):
    d = self.d
    txt = 'This city current has '
    for k, v in d.items():
      txt += str(v) + " " + str(k) + "; "
    return txt


  def __eq__(self,s2):
    if not (type(self)==type(s2)):
      return False
    d1 = self.d
    d2 = s2.d
    return d1==d2


  def __hash__(self):
    return (str(self)).__hash__()


  def __copy__(self):
    d1 = self.d
    news = {}

    for k, v in d1.items():
      news[k] = v
    return State(news)


  def getUnitEmmisionFor(self,factor):
    if factor == 'factory':
      return 910
    if factor == 'vehicle':
      return 120
    if factor == 'temple':
      return 44
    if factor == 'population':
      return 0.175

  def getUnitEconomyGrowthFor(self,factor):
    if factor == 'factory':
      return 500
    if factor == 'vehicle':
      return 10
    if factor == 'temple':
      return 50
    if factor == 'population':
      return 30

#</STATE>


#<COMMON_DATA>
MIN_POPULATION = 300
MAX_POPULATION = 30000

MIN_TEMPLES = 3

MIN_VEHICLE_POPULATION_RATIO = 0.2   # 1 car for five people
MIN_FACTORY_POPULATION_RATIO = 0.002 # 1 factory for 2000 K people

MAX_TEMPLE = 8
MAX_EMISSION = 30000

MIN_ECON = 100000
#</COMMON DATA>



#<INITIAL_STATE>
INITIAL_STATE = State({'factory': 2700, 'vehicle': 5610000, 'temple': 4,
                       'population': 20000000, "emission": 3500000, "economy": })
CREATE_INITIAL_STATE = lambda: INITIAL_STATE


#<OPERATORS>
combinations = [('factory',1),('factory',-1),
                ('vehicle',1),('vehicle',-1),
                ('temple',1),('temple',-1),
                ('population', 10)]

OPERATORS = [Operator("Change "+ p + " for " + str(q) + " unit",
                      lambda s, p1=p, q1=q: can_move(s, p1, q1),
                      lambda s, p1=p, q1=q: move(s, p1, q1))
             for (p,q) in combinations]


#<GOAL_TEST>
GOAL_TEST = lambda s: goal_test(s)

#<GOAL_MESSAGE_FUNCTION>
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)

#<HEURISTICS_HASH>
HEURISTICS = {'h1': h1}