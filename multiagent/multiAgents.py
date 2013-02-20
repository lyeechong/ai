# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"

    score = 10000
    if successorGameState.isWin():
      return 100000000
    for ghost in newGhostStates:
      ghostPos = ghost.getPosition()
      if util.manhattanDistance(ghostPos, newPos) < 2:
        score -= 10000
      else:
        score += util.manhattanDistance(ghostPos, newPos) * 1
        
    nearFood = 1000
    farFood = 1000
    for foodPos in oldFood.asList():
      dist = util.manhattanDistance(foodPos, newPos)
      if (dist < nearFood):
        nearFood = dist
      if (dist > farFood):
        farFood = dist
    if (currentGameState.getNumFood() < successorGameState.getNumFood()):
      score += 5

    if action == Directions.WEST:
      score -= 1
    if action == Directions.STOP:
      score -= 2
        
    for scareTime in newScaredTimes:
      score += scareTime * 1

    score -= 2 * farFood
    score -= 5 * nearFood
    capsuleplaces = currentGameState.getCapsules()
    if successorGameState.getPacmanPosition() in capsuleplaces:
        score += 5
    return max(score, 0)
    
    #their original return
    #return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"

    def MaxValue(gameState, currentDepth, agentNumber):
       
      if currentDepth is self.depth or gameState.isWin() or gameState.isLose():
    
        #print 'evaluation function at leaf ',self.evaluationFunction(gameState)
        return (self.evaluationFunction(gameState), Directions.NORTH)
      #print 'depth ',currentDepth
        
      largestValue = float("-inf")
      bestAction = Directions.NORTH
      for action in gameState.getLegalActions(agentNumber):
        #print 'analyzing ',action,' for pacman ',agentNumber
        successor = gameState.generateSuccessor(agentNumber, action)
        successorValue = MinValue(successor, currentDepth, (agentNumber + 1) % gameState.getNumAgents())[0]
        if(successorValue > largestValue):
          largestValue = successorValue
          bestAction = action
      return (largestValue, bestAction)
      
    def MinValue(gameState, currentDepth, agentNumber):
      if currentDepth is self.depth or gameState.isWin() or gameState.isLose():
        #print 'evaluation function at leaf ',self.evaluationFunction(gameState)
        return (self.evaluationFunction(gameState), Directions.NORTH)
       
      #print 'depth ',currentDepth
      
      smallestValue = float("inf")
      bestAction = Directions.NORTH 
      for action in gameState.getLegalActions(agentNumber):
        #print 'analyzing ',action,' for ghost ',agentNumber
        successor = gameState.generateSuccessor(agentNumber, action)
        nextAgentNumber = (agentNumber + 1) % gameState.getNumAgents()
        if nextAgentNumber is 0:
          successorValue = MaxValue(successor, currentDepth + 1, nextAgentNumber)[0]
        else:
          successorValue = MinValue(successor, currentDepth, nextAgentNumber)[0]
        if(successorValue < smallestValue):
          smallestValue = successorValue
          bestAction = action
      return (smallestValue, bestAction)

    result = MaxValue(gameState, 0, 0)
    resultActionToTake = result[1]
    #print 'Minimax value for depth ', self.depth,' ',result[0]
    #import time
    #time.sleep(1000000)
    return resultActionToTake


class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    
    def MaxValue(gameState, currentDepth, agentNumber, alpha, beta):
      if currentDepth is self.depth or gameState.isWin() or gameState.isLose():
        return (self.evaluationFunction(gameState), Directions.NORTH)
        
      largestValue = float("-inf")
      bestAction = Directions.NORTH
      for action in gameState.getLegalActions(agentNumber):
        successor = gameState.generateSuccessor(agentNumber, action)
        nextAgentNumber = (agentNumber + 1) % gameState.getNumAgents()
        successorValue = MinValue(successor, currentDepth, nextAgentNumber, alpha, beta)[0]
        if(successorValue >= beta):
          return (successorValue, action)
        alpha = max(alpha, successorValue)
        if(successorValue > largestValue):
          largestValue = successorValue
          bestAction = action
      return (largestValue, bestAction)
      
    def MinValue(gameState, currentDepth, agentNumber, alpha, beta):
      if currentDepth is self.depth or gameState.isWin() or gameState.isLose():
        return (self.evaluationFunction(gameState), Directions.NORTH)
      
      smallestValue = float("inf")
      bestAction = Directions.NORTH 
      for action in gameState.getLegalActions(agentNumber):
        successor = gameState.generateSuccessor(agentNumber, action)
        nextAgentNumber = (agentNumber + 1) % gameState.getNumAgents()
        if nextAgentNumber is 0:
          successorValue = MaxValue(successor, currentDepth + 1, nextAgentNumber, alpha, beta)[0]
        else:
          successorValue = MinValue(successor, currentDepth, nextAgentNumber, alpha, beta)[0]
        if(successorValue <= alpha):
          return (successorValue, action)
        beta = min(beta, successorValue)
        if(successorValue < smallestValue):
          smallestValue = successorValue
          bestAction = action
      return (smallestValue, bestAction)

    alpha = float("-inf")
    beta = float("inf")      
    result=MaxValue(gameState, 0, 0, alpha, beta)
    resultActionToTake = result[1]
    #import time
    #print 'AlphaBeta value for depth ', self.depth,' ',result[0]
    #time.sleep(1000)
    return resultActionToTake


class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    
    #print "\n\n\n"
    
    def MaxValue(gameState, currentDepth, agentNumber):
      if currentDepth is self.depth or gameState.isWin() or gameState.isLose():
        #print "\t", self.evaluationFunction(gameState)
        return (self.evaluationFunction(gameState), Directions.STOP)
        
      largestValue = float("-inf")
      bestAction = Directions.STOP
      legalActions = gameState.getLegalActions(agentNumber)
      legalActions.sort()
      for action in legalActions:
        if action is Directions.STOP:
          continue
        successor = gameState.generateSuccessor(agentNumber, action)
        nextAgentNumber = (agentNumber + 1) % gameState.getNumAgents()
        if nextAgentNumber is 0:
            successorValue= MaxValue(successor, currentDepth + 1, nextAgentNumber)[0]
        else:
            successorValue = ExpValue(successor, currentDepth, (agentNumber + 1) % gameState.getNumAgents())[0]
        if(successorValue > largestValue):
          largestValue = successorValue
          bestAction = action
      return (largestValue, bestAction)
      
    def ExpValue(gameState, currentDepth, agentNumber):
      if currentDepth is self.depth or gameState.isWin() or gameState.isLose():
        #print "\t", self.evaluationFunction(gameState)
        return (self.evaluationFunction(gameState), Directions.STOP)
      
      totalValue = 0
      legalActions = gameState.getLegalActions(agentNumber)
      legalActions.sort()
      for action in legalActions:
        successor = gameState.generateSuccessor(agentNumber, action)
        nextAgentNumber = (agentNumber + 1) % gameState.getNumAgents()
        if nextAgentNumber is 0:
          successorValue = MaxValue(successor, currentDepth + 1, nextAgentNumber)[0]
        else:
          successorValue = ExpValue(successor, currentDepth, nextAgentNumber)[0]
        totalValue += successorValue
      return (totalValue/len(legalActions), Directions.STOP)
      
    result= MaxValue(gameState, 0, 0)
    resultActionToTake =result[1]
    
    #print gameState.getLegalActions(0)
    #print 'AlphaBeta value for depth ', self.depth,' ',result[0]
    import time

    #print "SCORE picked ", result[0]
    #time.sleep(1)
    #print 'This should always be true... ', resultActionToTake in gameState.getLegalActions(0)
    return resultActionToTake

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    
    
    ---------------- OUR DESCRIPTION HERE! ---------------- 
    
    First off, our code used a linear addition scorer to figure out the
    utility of the gameState, and we used mutipliers based on the
    value of a feature in the state (example, food was good).
    
    Our code made it so that dying was considered bad and had a high negative score.
    We then based all our other values on the dying score.
    
    We valued winning, but we did not make it a really high number since
    you could easily grab more points via eating ghosts first before winning, and
    we took that into account.
    
    When pacman encountered a ghost, we took into consideration the number of ghosts nearby
    and the state of the ghosts.
    
    If the ghost was scared, and the scared timer was greater than the distance pacman is to the
    ghost, we would increase the score the closer pacman got to it (try and eat it).
    
    If the ghosts nearby were not scared, we would check to see the distance of the nearest
    power-pellet, and see if we could reach it before the ghost reached us, if so, head for the pellet
    (then go eat the ghosts).
    
    If there were no pellets, and the ghosts nearby were not scared, our logic depended on the number of
    ghosts.
       If there is one ghost, we would simply not go into its square, as pacman can easily dodge a
        single ghost all day since he gets the first move.
       If there is more than one ghost nearby, pacman would avoid them, being penalized for
        being too close.
    
    For food, we would just head to the nearest food.
    
    If we saw our score was less than 500 and we were going to lose, we made it so that pacman would
    try and stay alive instead of suiciding as we found most of the time pacman could have made it out
    alive.
    
    We had plenty of issues with pacman thrashing around and we never really completely solved it, but
    we managed to mitigate most of the problem by using the ghosts' positons to randomize pacman's actions.
    We also made it so that pacman would favor going South and West over North and East to help him get
    unstuck.
    
    We made it so that eating capsules and food added to the score.
    
    We also used the in-game score method < currentGameState.getScore() > as the main component of our
    scoring method, and our actual score just being used mainly to break ties.
    
    It works pretty well and four out of five times we get an average score greater than 1000.
    
    ---------------- END OUR DESCRIPTION HERE ---------------- 
    
    
  """
  "*** YOUR CODE HERE ***"
  
  pacmanPosition = currentGameState.getPacmanPosition()
  oldFood = currentGameState.getFood()
  newGhostStates = currentGameState.getGhostStates()
  capsulePositions = currentGameState.getCapsules()
  
  #print "current pacman position ", pacmanPosition

  score = 0
  
  numGhostsNear = 0
  numGhostsScared = 0
  
  if currentGameState.isLose():
    score -= 1000000000
  if currentGameState.isWin() and numGhostsScared is 0:
    score += 100000000
  
  for ghost in newGhostStates: 
    ghostScareTimer = ghost.scaredTimer
    if ghostScareTimer > 2:
      numGhostsScared += 1
  
  for ghost in newGhostStates:
    ghostPosition = ghost.getPosition()
    ghostScareTimer = ghost.scaredTimer
    ghostDistanceToPacman = util.manhattanDistance(ghostPosition, pacmanPosition)
        
    #if the ghost is near pacman...
    if ghostDistanceToPacman < 5:
      #check to see if the ghost is scared
      if ghostScareTimer >= ghostDistanceToPacman:
      
        #if the ghost will be scared long enough for pacman to eat it, chase
        #this will reward pacman for being closer to the scared ghost
        
        if ghostDistanceToPacman is 0:
          #right ontop of the ghost, lots of points!
          #KILL IT WITH FIRE
          score += 100000000000000000000000000000000000000000000000
        else:
          score += 80000/(ghostDistanceToPacman+1)
          
      else:
        #the ghost is either scared but too far, or not scared
        #mm... before running, check to see if there's a nearby power pellet...
        if pacmanPosition in capsulePositions:
          #is pacman on a power pellet? how convenient!
          score += 200000
          
        noNearbyPellets = True
        for pellet in capsulePositions:
          pelletDistanceToPacman = util.manhattanDistance(pellet, pacmanPosition)
          if ghostDistanceToPacman >= pelletDistanceToPacman:
            #the ghost is further away from this pellet
            #head to the pellet!
            if pelletDistanceToPacman is 0:
              score += 100400
            else:
              score += 100000/pelletDistanceToPacman
        if noNearbyPellets:
          if ghostDistanceToPacman < 4:
            numGhostsNear += 1
            
    score += ghostPosition[0] * 1000 - ghostPosition[1] * 1500
  
  if numGhostsNear > 1:
    for ghost in newGhostStates:
      ghostPosition = ghost.getPosition()
      ghostDistanceToPacman = util.manhattanDistance(ghostPosition, pacmanPosition)
      if ghostDistanceToPacman is 0:
        score -= 1000000000
      else:
        if ghostDistanceToPacman is 0:
          score -= 1000000000
        else:
          score -= 1000000000/(ghostDistanceToPacman+1)
    
  #look for the nearest food pellet (which is not at pacman's location) and the furthest
  nearestFoodDistance = float("inf")
  
  temp = oldFood.asList()
  import random
  #random.shuffle(temp)
  temp.sort()
  for foodPosition in temp:
    foodDistanceToPacman = util.manhattanDistance(foodPosition, pacmanPosition)
    #print foodPosition, pacmanPosition, foodDistanceToPacman
    if foodDistanceToPacman is 0:
      #pacman is on some food, reward him!
      score += 20000
      continue
    if (foodDistanceToPacman < nearestFoodDistance) and (foodDistanceToPacman > 0):
      nearestFoodDistance = foodDistanceToPacman
  
  score += 8000/(pacmanPosition[1]+1)
  score += 8000/(pacmanPosition[0]+1)
  
  #print "nearestFoodDistance ", nearestFoodDistance
  
  import time
  #time.sleep(1000)
  temp = (100000 / nearestFoodDistance)
  #print "AGHGHHGHGHGHGHGHGG ", temp
  score += temp
  
  if currentGameState.getScore() < 500:
    if currentGameState.isLose():
      score -= 100000000000000000
    
  score += currentGameState.getScore()*1000000
  
  score -= 10000 * len(oldFood.asList())
  score -= 50000 * len(capsulePositions)
  
  
  #print score
  
  
  
  return score

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    def betterEvaluationFunction(currentGameState):
      """
        Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
        evaluation function (question 5).

        DESCRIPTION: <write something here so we know what you did>
      
      """
      "*** YOUR CODE HERE ***"
      
      pacmanPosition = currentGameState.getPacmanPosition()
      oldFood = currentGameState.getFood()
      newGhostStates = currentGameState.getGhostStates()
      capsulePositions = currentGameState.getCapsules()
      
      #print "current pacman position ", pacmanPosition

      score = 0
      
      numGhostsNear = 0
      numGhostsScared = 0
      
      if currentGameState.isLose():
        score -= 1000000000
      if currentGameState.isWin() and numGhostsScared is 0:
        score += 100000000
      
      for ghost in newGhostStates: 
        ghostScareTimer = ghost.scaredTimer
        if ghostScareTimer > 2:
          numGhostsScared += 1
      
      for ghost in newGhostStates:
        ghostPosition = ghost.getPosition()
        ghostScareTimer = ghost.scaredTimer
        ghostDistanceToPacman = util.manhattanDistance(ghostPosition, pacmanPosition)
            
        #if the ghost is near pacman...
        if ghostDistanceToPacman < 5:
          #check to see if the ghost is scared
          if ghostScareTimer >= ghostDistanceToPacman:
          
            #if the ghost will be scared long enough for pacman to eat it, chase
            #this will reward pacman for being closer to the scared ghost
            
            if ghostDistanceToPacman is 0:
              #right ontop of the ghost, lots of points!
              #KILL IT WITH FIRE
              score -= 1000000000000
            else:
              score -= 8000000/(ghostDistanceToPacman+1)
              
          else:
            #the ghost is either scared but too far, or not scared
            #mm... before running, check to see if there's a nearby power pellet...
            if pacmanPosition in capsulePositions:
              #is pacman on a power pellet? how convenient!
              score += 200000
              
            noNearbyPellets = True
            for pellet in capsulePositions:
              pelletDistanceToPacman = util.manhattanDistance(pellet, pacmanPosition)
              if ghostDistanceToPacman >= pelletDistanceToPacman:
                #the ghost is further away from this pellet
                #head to the pellet!
                if pelletDistanceToPacman is 0:
                  score += 100400
                else:
                  score += 100000/pelletDistanceToPacman
            if noNearbyPellets:
              if ghostDistanceToPacman < 4:
                numGhostsNear += 1
                
        score += ghostPosition[0] * 1000 - ghostPosition[1] * 1500
      
      if numGhostsNear > 1:
        for ghost in newGhostStates:
          ghostPosition = ghost.getPosition()
          ghostDistanceToPacman = util.manhattanDistance(ghostPosition, pacmanPosition)
          if ghostDistanceToPacman is 0:
            score -= 1000000000
          else:
            if ghostDistanceToPacman is 0:
              score -= 1000000000
            else:
              score -= 1000000000/(ghostDistanceToPacman+1)
        
      #look for the nearest food pellet (which is not at pacman's location) and the furthest
      nearestFoodDistance = float("inf")
      
      temp = oldFood.asList()
      import random
      #random.shuffle(temp)
      temp.sort()
      for foodPosition in temp:
        foodDistanceToPacman = util.manhattanDistance(foodPosition, pacmanPosition)
        #print foodPosition, pacmanPosition, foodDistanceToPacman
        if foodDistanceToPacman is 0:
          #pacman is on some food, reward him!
          score += 20000
          continue
        if (foodDistanceToPacman < nearestFoodDistance) and (foodDistanceToPacman > 0):
          nearestFoodDistance = foodDistanceToPacman
      
      score += 8000/abs(20-pacmanPosition[1]+1)
      score += 8000/(pacmanPosition[0]+1)
      
      #print "nearestFoodDistance ", nearestFoodDistance
      
      import time
      #time.sleep(1000)
      temp = (100000 / nearestFoodDistance)
      #print "AGHGHHGHGHGHGHGHGG ", temp
      score += temp
      
      if currentGameState.getScore() < 500:
        if currentGameState.isLose():
          score -= 100000000000000000
        
      score += currentGameState.getScore()*1000000
      
      score -= 10000 * len(oldFood.asList())
      score -= 50000 * len(capsulePositions)
      
      
      #print score
      
      
      
      return score
    def MaxValue(gameState, currentDepth, agentNumber, alpha, beta):
      if currentDepth is self.depth or gameState.isWin() or gameState.isLose():
        return (betterEvaluationFunction(gameState), Directions.NORTH)
        
      largestValue = float("-inf")
      bestAction = Directions.NORTH
      for action in gameState.getLegalActions(agentNumber):
        if action is Directions.STOP:
          continue
        successor = gameState.generateSuccessor(agentNumber, action)
        nextAgentNumber = (agentNumber + 1) % gameState.getNumAgents()
        successorValue = MinValue(successor, currentDepth, nextAgentNumber, alpha, beta)[0]
        if(successorValue >= beta):
          return (successorValue, action)
        alpha = max(alpha, successorValue)
        if(successorValue > largestValue):
          largestValue = successorValue
          bestAction = action
      return (largestValue, bestAction)
      
    def MinValue(gameState, currentDepth, agentNumber, alpha, beta):
      if currentDepth is self.depth or gameState.isWin() or gameState.isLose():
        return (betterEvaluationFunction(gameState), Directions.NORTH)
      
      smallestValue = float("inf")
      bestAction = Directions.NORTH 
      for action in gameState.getLegalActions(agentNumber):
        successor = gameState.generateSuccessor(agentNumber, action)
        nextAgentNumber = (agentNumber + 1) % gameState.getNumAgents()
        if nextAgentNumber is 0:
          successorValue = MaxValue(successor, currentDepth + 1, nextAgentNumber, alpha, beta)[0]
        else:
          successorValue = MinValue(successor, currentDepth, nextAgentNumber, alpha, beta)[0]
        if(successorValue <= alpha):
          return (successorValue, action)
        beta = min(beta, successorValue)
        if(successorValue < smallestValue):
          smallestValue = successorValue
          bestAction = action
      return (smallestValue, bestAction)

    alpha = float("-inf")
    beta = float("inf")      
    result=MaxValue(gameState, 0, 0, alpha, beta)
    resultActionToTake = result[1]
    #import time
    #print 'AlphaBeta value for depth ', self.depth,' ',result[0]
    #time.sleep(1000)
    return resultActionToTake
    
    
    

