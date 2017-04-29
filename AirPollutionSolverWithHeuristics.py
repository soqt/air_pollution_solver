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


def can_move(s,factor,units):
  try:
    currentUnitsForFactor = s.getNumberOf(factor)
    if factor == 'greenbelt':
      return True

    if factor == 'population':
      if s.getNumberOf('population') + units > MAX_POPULATION: return False
      ratio = s.getNumberOf('factory') / (s.getNumberOf('population') + units)
      if ratio < BALANCED_FACTORY_POPULATION_RATIO: return False

    if factor == 'temple':
      newTemple = currentUnitsForFactor + units
      if newTemple < MIN_TEMPLES or newTemple > MAX_TEMPLE: return False

    if factor == 'vehicle':
      ratio = (currentUnitsForFactor + units)/ s.getNumberOf('population')
      if ratio < MIN_VEHICLE_POPULATION_RATIO: return False
      if ratio > MAX_VEHICLE_POPULATION_RATIO: return False

    if factor == 'factory':
      if units > 0:
        ratio = (currentUnitsForFactor + units) / s.getNumberOf('population')
        if ratio > BALANCED_FACTORY_POPULATION_RATIO: return True
        else: return False
      if units < 0:
        ratio = (currentUnitsForFactor + units) / s.getNumberOf('population')
        if ratio < BALANCED_FACTORY_POPULATION_RATIO: return False



    newEmission = s.getEmission() + units * s.getUnitEmissionFor(factor)
    if newEmission > MAX_EMISSION: return False
    newEconomy = s.getEconomy() + units * s.getUnitEconomyGrowthFor(factor)
    if newEconomy < s.getEconomy() * 0.7: return False

    if newEmission/newEconomy > INITIAL_RATIO: return False

    return True


    # if current economy decreases too much, return false

    # debugging
    # print(currentEmission/currentEcon)
    # print(newEmission/newEcon)
    # /debugging

  except (Exception) as e:
    print(e)



def move(s,factor,unit):
  news = s.__copy__()
  d = news.d
  d[factor] += unit
  d['economy'] = d['economy'] + s.getUnitEconomyGrowthFor(factor) * unit
  d['emission'] = d['emission'] + s.getUnitEmissionFor(factor) * unit


  return news



def goal_test(s):
  return (s.d['emission'] / s.d['economy'] <= GOAL_RATIO)
  # return s.d['emission'] == 0

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
  return (emi/eco - GOAL_RATIO) * 1000000000



#<STATE>#
class State():
  def __init__(self,d):
    self.d = d

  def __str__(self):
    d = self.d
    txt = 'This city current has '
    for k, v in d.items():
      txt += str(v) + " " + str(k) + ", "
    txt += " with emission of " + str(d['emission']) + " tons and annual GDP $" + str(d['economy']) + "."
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

  def getNumberOf(self, factor):
    d = self.d
    if factor == 'factory':
      return d['factory']
    if factor == 'vehicle':
      return d['vehicle']
    if factor == 'temple':
      return d['temple']
    if factor == 'population':
      return d['population']
    if factor == 'greenbelt':
      return d['greenbelt']
    return None

  def getEmission(self):
    d = self.d
    return d['emission']

  def getEconomy(self):
    d = self.d
    return d['economy']

  def getUnitEmissionFor(self,factor):
    if factor == 'factory':
      return 910
    if factor == 'vehicle':
      return 0.12
    if factor == 'temple':
      return 44
    if factor == 'population':
      return 0.075
    if factor == 'greenbelt':
      return -10
    return None

  def getUnitEconomyGrowthFor(self,factor):
    if factor == 'factory':
      return 50000000
    if factor == 'vehicle':
      return 20000
    if factor == 'temple':
      return 5000000
    if factor == 'population':
      return 100000
    if factor == 'greenbelt':
      return -500000
    return None

#</STATE>


#<INITIAL_STATE>
INITIAL_STATE = State({
  'factory': 2700, 'vehicle': 5610000, 'temple': 4, 'greenbelt': 500,'population': 20000000,
  "emission": 3105476, "economy": 2246970000000
})
CREATE_INITIAL_STATE = lambda: INITIAL_STATE

#<COMMON_DATA>
INITIAL_RATIO = INITIAL_STATE.getEmission()/INITIAL_STATE.getEconomy()
GOAL_RATIO = INITIAL_RATIO * 0.7

MAX_EMISSION = INITIAL_STATE.getEmission() * 1.2

MAX_POPULATION = INITIAL_STATE.getNumberOf('population') * 1.5

MIN_TEMPLES = 3
MAX_TEMPLE = 8

MIN_VEHICLE_POPULATION_RATIO = 0.1   # on average 1 car per 10 people
MAX_VEHICLE_POPULATION_RATIO = 0.7  # on average 7 car serves 10 people


MAX_FACTORY_POPULATION_RATIO = INITIAL_STATE.getNumberOf('factory') / INITIAL_STATE.getNumberOf('population')
BALANCED_FACTORY_POPULATION_RATIO = 0.00005 # on average 5 factory for 100 K people



#</COMMON DATA>



#<OPERATORS>
combinations = [('factory',1),('factory',-1),
                ('vehicle',1),('vehicle',-1),
                ('temple',1),('temple',-1),
                ('population', 100000), ('greenbelt',1), ('greenbelt', - 1)]

OPERATORS = [Operator("Change "+ p + " : " + str(q) + " unit",
                      lambda s, p1=p, q1=q: can_move(s, p1, q1),
                      lambda s, p1=p, q1=q: move(s, p1, q1))
             for (p,q) in combinations]


#<GOAL_TEST>
GOAL_TEST = lambda s: goal_test(s)

#<GOAL_MESSAGE_FUNCTION>
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)

#<HEURISTICS_HASH>
HEURISTICS = [h1]
