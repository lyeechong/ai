# baselineAgents.py
# -----------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from captureAgents import CaptureAgent
from captureAgents import AgentFactory
import distanceCalculator
import random, time, util
from game import Directions
import keyboardAgents
import game
from util import nearestPoint

#############
# FACTORIES #
#############

NUM_KEYBOARD_AGENTS = 0
class BaselineAgents(AgentFactory):
  "Returns one keyboard agent and offensive reflex agents"

  def __init__(self, isRed, first='offense', second='defense', rest='offense'):
    AgentFactory.__init__(self, isRed)
    #self.agents = [first, second]
    # -- change to all offensive agents since I haven't worked on the defensive yet
    self.agents = ['offense', 'offense']
    self.rest = rest
    self.isRed = isRed

  def getAgent(self, index):
    if len(self.agents) > 0:
      return self.choose(self.agents.pop(0), index)
    else:
      return self.choose(self.rest, index)

  def choose(self, agentStr, index):
    if agentStr == 'keys':
      global NUM_KEYBOARD_AGENTS
      NUM_KEYBOARD_AGENTS += 1
      if NUM_KEYBOARD_AGENTS == 1:
        return keyboardAgents.KeyboardAgent(index)
      elif NUM_KEYBOARD_AGENTS == 2:
        return keyboardAgents.KeyboardAgent2(index)
      else:
        raise Exception('Max of two keyboard agents supported')
    elif agentStr == 'offense':
      return OffensiveReflexAgent(index)
    elif agentStr == 'defense':
      return DefensiveReflexAgent(index)
    else:
      raise Exception("No staff agent identified by " + agentStr)

class AllOffenseAgents(AgentFactory):
  "Returns one keyboard agent and offensive reflex agents"

  def __init__(self, **args):
    AgentFactory.__init__(self, **args)

  def getAgent(self, index):
    return OffensiveReflexAgent(index)

class OffenseDefenseAgents(AgentFactory):
  "Returns one keyboard agent and offensive reflex agents"

  def __init__(self, **args):
    AgentFactory.__init__(self, **args)
    self.offense = False

  def getAgent(self, index):
    self.offense = not self.offense
    if self.offense:
      return OffensiveReflexAgent(index)
    else:
      return DefensiveReflexAgent(index)

##########
# Agents #
##########

class ReflexCaptureAgent(CaptureAgent):
  """
  A base class for reflex agents that chooses score-maximizing actions
  """
  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    actions = gameState.getLegalActions(self.index)

    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

    return random.choice(bestActions)

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights

  def getFeatures(self, gameState, action):
    """
    Returns a counter of features for the state
    """
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)
    return features

  def getWeights(self, gameState, action):
    """
    Normally, weights do not depend on the gamestate.  They can be either
    a counter or a dictionary.
    """
    return {'successorScore': 1.0}

class OffensiveReflexAgent(ReflexCaptureAgent):
  """
  A reflex agent that seeks food. This is an agent
  we give you to get an idea of what an offensive agent might look like,
  but it is by no means the best or only way to build an offensive agent.
  """
  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)

    currentPosition = gameState.getAgentState(self.index).getPosition()
    currentX = currentPosition[0]
    currentY = currentPosition[1]

    # -- Note: call the isAPacman thing on the successor since you can change
    # --       when going across the border
    successor = self.getSuccessor(gameState, action)
    isAPacman = successor.getAgentState(self.index).isPacman
    isAGhost = not isAPacman # -- redundant?

    ######################################################
    # -- The idea behind the agent is
    # -- to try a divide and conquer 
    # -- approach since otherwise
    # -- the two agents
    # -- bunch up in the same area, which is inefficient
    ######################################################
    
    # -- this is the dividing up the enemy zone part
    sector = self.index / 2

    # -- insert informertial here: "THERE'S GOTTA BE A BETTER WAY TO DO THIS!"
    # -- probably could use getSuccessor, but I'm too lazy to rewrite the code
    if action is Directions.STOP:
      movementVector = (0,0)
    elif action is Directions.NORTH:
      movementVector = (0,1)
    elif action is Directions.EAST:
      movementVector = (1,0)
    elif action is Directions.SOUTH:
      movementVector = (0,-1)
    elif action is Directions.WEST:
      movementVector = (-1,0)
    
    
    xMoveToSuccessor, yMoveToSuccessor = movementVector
    successorXPos = currentX + xMoveToSuccessor
    successorYPos = currentY + yMoveToSuccessor
    successorPos = (successorXPos, successorYPos)
    
    # -- their food code, modified so the agents target the food in
    # -- the sector they are responsible for
    # Compute distance to the nearest food
    foodList = self.getFood(successor).asList()
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      myPos = successor.getAgentState(self.index).getPosition()
      
      # -- find the closest piece of food in the agent's sector
      smallestOverall = 1000000
      smallestInSector = 1000000
      for foodPosition in foodList:
        distanceToFoodPiece = self.getMazeDistance(successorPos, foodPosition)
        # -- check to see if it's in the agent's designated sector
        foodY = foodPosition[1]
        heightOfLayout = gameState.getWalls().height
        
        # -- this is a constant right now... may want to change
        numFriendlies = 2
        
        sectorTopY = (sector + 1) * heightOfLayout/numFriendlies
        sectorBottomY = sector * heightOfLayout/numFriendlies
        if foodY > sectorBottomY and foodY < sectorTopY:
          smallestInSector = min(distanceToFoodPiece, smallestInSector)
        smallestOverall = min(distanceToFoodPiece, smallestOverall)
      
      # -- checking if there was no food left in the agent's sector
      if smallestInSector is 1000000:
        smallestInSector = smallestOverall
      
      features['distanceToFood'] = smallestInSector
    
    # -- capsule checking
    # -- right now does not take into account if there are ghosts nearby or not
    for capsuleXPos, capsuleYPos in gameState.getCapsules():
      if successorXPos is capsuleXPos and successorYPos is capsuleYPos and isPacman:
        features['capsuleEaten'] = 1.0

    # -- Ghost checking stuff, how close they are and if they're scared
    #currentObsGameState = getCurrentObservation()
    # -- using gameState instead of current observation... I think they're the same
    for enemyAgentIndex in self.getOpponents(gameState):
      enemyAgent = gameState.getAgentState(enemyAgentIndex)
      enemyPosition = enemyAgent.getPosition()
      enemyScaredTimer = enemyAgent.scaredTimer
      
      if enemyPosition is None:
        # -- not sure, but this happens often
        # -- probably due to the noisy distances!
        # -- we definitely don't want None positions
        continue;
      
      # -- check if the enemy is on top of us!
      if self.getMazeDistance(enemyPosition, successorPos) is 0:  
        # -- if they are, see if they're scared
        if enemyScaredTimer > 0:
          # -- they're harmless...
          # -- we get no points for eating them, so leave them be
          features['scaredEnemies1PosAway'] += 1
        else:
          # -- they're dangerous!
          features['lethalEnemies1PosAway'] += 1
      elif self.getMazeDistance(enemyPosition, successorPos) is 1:
        # -- if they are, see if they're scared
        if enemyScaredTimer > 0:
          # -- they're harmless...
          # -- we get no points for eating them, so leave them be
          features['scaredEnemies2PosAway'] += 1
        else:
          # -- they're dangerous!
          features['lethalEnemies2PosAway'] += 1
          
      # -- right now I'm not going to bother to check if they are more than 1 spot
      # -- away since we have shown that pacman is awesome at dodging one ghost
      # -- and if they use two ghosts.. they can't kill both of ours at the same time!
    return features
    
    

  def getWeights(self, gameState, action):
    # -- Note: call the isAPacman thing on the successor since you can change
    # --       when going across the border
    successor = self.getSuccessor(gameState, action)
    isAPacman = successor.getAgentState(self.index).isPacman
    if isAPacman:
      return {'successorScore': 100, 'distanceToFood': -1, 'capsuleEaten': 10, 'scaredEnemies1PosAway': 1, 'lethalEnemies1PosAway':-10, 'scaredEnemies2PosAway': 0, 'lethalEnemies2PosAway':-3}
    else:
      return {'successorScore': 100, 'distanceToFood': -1, 'capsuleEaten': 0, 'scaredEnemies1PosAway': 100, 'lethalEnemies1PosAway':100, 'scaredEnemies2PosAway': 50, 'lethalEnemies2PosAway':50}

class DefensiveReflexAgent(ReflexCaptureAgent):
  """
  A reflex agent that keeps its side Pacman-free. Again,
  this is to give you an idea of what a defensive agent
  could be like.  It is not the best or only way to make
  such an agent.
  """

  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    # Computes whether we're on defense (1) or offense (0)
    features['onDefense'] = 1
    if myState.isPacman: features['onDefense'] = 0

    # Computes distance to invaders we can see
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      features['invaderDistance'] = min(dists)

    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1

    return features

  def getWeights(self, gameState, action):
    return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}


