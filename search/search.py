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
  
  import time

  currentPath = []
  visited = [] #a list of visited spots, so we don't go around in circles...
  
  startState = problem.getStartState()
  visited.append(startState)

  once = True
  
  print "Init spot ", startState
  
  #start the loop...
  print "Cometh, the while loop!"
  
  done = False
  
  while(not done):
    #check to see if we're at the finish!
    
    print "while loop begin", once
    
    if not once:
      print "Curr spot ", currentPath[-1][0]
    
    if once and problem.isGoalState(startState):
        print "Done 1 hit!"
        done = True
        break
    elif not once and problem.isGoalState(currentPath[-1][0]):
      print "Done 2 hit!"
      #we're done!
      done = True
      break
    else:
      #otherwise... we're not!
      print "hit the else"
      
      if once:
        successors = problem.getSuccessors(startState)
      else:
        successors = problem.getSuccessors(currentPath[-1][0])
      
      notVisited = 0
      print "starting for loop seach for a successor"
      for choice in successors:
        print "\tchoice[0] ", choice[0], "\n\tvisited ", visited
        if not choice[0] in visited:
          print "Found successor ", choice[0]
          notVisited = choice
          break
      
      while notVisited is 0:
        print "Could not find avail successors, time to pop! "
        print "Popped ", currentPath.pop()[0]
        successors = problem.getSuccessors(currentPath[-1][0])
        notVisited = 0
        for choice in successors:
          if not choice[0] in visited:
            notVisited = choice
            break
      
      print "Adding to the path, ", notVisited[0]
      currentPath.append(notVisited)
      visited.append(notVisited[0])
      once = False
      
      print "--OUR CURRENT PATH-- :: "
      for pos in currentPath:
        print pos, ", "
      
      print "\nSleeping!"
#      time.sleep(1)
      print "Done sleeping!\n"
  
  print "Done with the big while loop!"
  
  #whew! we're out of the while loop!
  #hopefully we found the goal...
  
  #let's print the path we found to see if it's correct...
  #print "path stack ", currentPath

  path = [] #this is the path we will return
  
  while not len(currentPath) is 0:
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
