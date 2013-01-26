# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"
  
  #cross your fingers hope it works, it's depth first search and it has its quirks!
  #AGGGHHH PYTHON!
  
  from game import Directions
  n = Directions.NORTH
  e = Directions.EAST
  s = Directions.SOUTH
  w = Directions.WEST
  cardinalDirections = [n,e,s,w] #mmm... not used... yet
  
  import util #for the stack!
  currentPath = util.Stack()
  
  visited = [] #a list of visited spots, so we don't go around in circles...
  
  startState = problem.getStartState()
  print "The start state       : ", startState
  print "Is it the goal state? : ", problem.isGoalState(startState)
  print "The successors are    : ", problem.getSuccessors(startState)
  
  currentState = problem.getStartState() 
  visited.append(currentState)
  
  #start the loop...
  print "Cometh, the while loop!"
  done = False
  while(not done):
    print "Current state ", currentState
    print "Visited spots ", visited
    #check to see if we're at the finish!
    if problem.isGoalState(currentState):
      #we're done!
      done = True
      break
    else:
      #otherwise... we're not!
      successors = problem.getSuccessors(currentState)

      #we need to go deeper...
      for choice in successors:
        if choice[0] not in visited:
          currentPath.push(choice)
      
      if currentPath.isEmpty():
        #well... it's empty, which means we exhausted all the routes and didn't find the goal :(
        done = True
        break
        
      visited.append(currentState)
      pop = currentPath.pop()
      currentState = pop[0] #updates the new state to the last one pushed on the stack
  
  #whew! we're out of the while loop!
  #hopefully we found the goal...
  
  path = [] #this is the path we will return
  
  while not currentPath.isEmpty():
    item = currentPath.pop()[1]
    print "inserting item into path : ", item
    path.insert(0, item) #insert into the front of the list
    
  return path #yup! we're done!
      
  "end our code here!"

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
