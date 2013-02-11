import layout
from game import Agent
import searchAgents
from game import Actions
import pacman
import sys

foodTests = [
("Test 7",11, [
  "%%%%%",
  "%...%",
  "%...%",
  "%...%",
  "%P..%",
  "%%%%%"]),

("Test 6", 5, [
  "%%%%%",
  "% ..%",
  "% . %",
  "% P %",
  "% . %",
  "%%%%%"]),

("Test 5", 7, [
  "%%%%%",
  "% ..%",
  "% . %",
  "% P %",
  "%   %",
  "% . %",
  "%%%%%"]),

("Test 4", 5, [
  "%%%%%",
  "%...%",
  "%   %",
  "%   %",
  "%P  %",
  "%%%%%"]),                    

("Test 3", 6, [
  "%%%%%",
  "%.. %",
  "% %.%",
  "%.%%%",
  "%P  %",
  "%%%%%"]),                    

("Test 2", 7, [
  "%%%%%",
  "% . %",
  "%   %",
  "% P %",
  "%   %",
  "%   %",
  "% . %",
  "%%%%%"]),                    


("Test 1", 8, [
  "%%%%%",
  "%.  %",
  "%   %",
  "%.P %",
  "%   %",
  "%   %",
  "%.  %",
  "%%%%%"]),                                       

("Test 8", 1, [
  "%%%%%",
  "% . %",
  "% P %",
  "%   %",
  "%   %",
  "%   %",
  "%   %",
  "%%%%%"]),    

("Test 9", 5, [
  "%%%%%",
  "% . %",
  "%   %",
  "%   %",
  "%   %",
  "% . %",
  "% P %",
  "%%%%%"]),    

("Test 10", 31, [
  "%%%%%%%%%%%",
  "% ....... %",
  "% %%%%%%. %",
  "% ....... %",
  "% .%%%%%% %",
  "% ....... %",
  "% %%%%%%. %",
  "% ....... %",
  "% P       %",
  "%%%%%%%%%%%"]),

("Test 11", 21, [
  "%%%%%%%%%%%%%%%%%%%%%%%%",
  "%.    P .       ..     %",
  "%%%%%%%%%%%%%%%%%%%%%%%%"]),     
("Test 13", 7, [
  "%%%%%%%",
  "%.   .%",
  "%  P  %",
  "%%%%%%%"]),

("Test 12", 16, [
  "%%%%%%",
  "%....%",
  "% %%.%",
  "% %%.%",
  "%.P .%",
  "%.%%%%",
  "%....%",
  "%%%%%%"])]


def foodConsistency(layoutText, cost, heuristic):  
  gameState = pacman.GameState()
  lay = layout.Layout(layoutText)
  gameState.initialize(lay, 0)
  problem = searchAgents.FoodSearchProblem(gameState)
  state = problem.getStartState()
  
  h0 = heuristic(state, problem)
  succs = problem.getSuccessors(state)
  for succ in succs:
    h1 = heuristic(succ[0], problem)
    if h0 - h1 > 1: return False
  return True

def foodAdmissible(layoutText, cost, heuristic): 
  gameState = pacman.GameState()
  lay = layout.Layout(layoutText)
  gameState.initialize(lay, 0)
  problem = searchAgents.FoodSearchProblem(gameState)
  startState = problem.getStartState()
  return heuristic(startState, problem) <= cost


def getStartState(layoutName):
  s = pacman.GameState()
  lay1 = layout.getLayout(layoutName,3)
  s.initialize(lay1, 0)
  return s

"Tests food search heuristic"
heuristic = searchAgents.foodHeuristic

for name, cost, lay in foodTests:
  if not foodAdmissible(lay, cost, heuristic):
    print 'Food heuristic failed admissibility test %s' % name
    sys.exit(1)
  else:
    print 'Passed admissibility test %s' % name

lay = 'trickySearch'
gameState = getStartState(lay)
problem = searchAgents.FoodSearchProblem(gameState)
if heuristic(problem.getStartState(), problem) > 60: 
  print 'Food heuristic failed admissibility test trickySearch'
  sys.exit(1)
  

for name, cost, lay in foodTests:
  if not foodConsistency(lay, cost, heuristic):
    print 'Food heuristic failed consistency test %s' % name
    sys.exit(1)
  else:
    print 'Passed consistency test %s' % name

