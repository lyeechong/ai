# inference.py
# ------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import util
import random
import busters
import game

class InferenceModule:
  """
  An inference module tracks a belief distribution over a ghost's location.
  This is an abstract class, which you should not modify.
  """
  
  ############################################
  # Useful methods for all inference modules #
  ############################################
  
  def __init__(self, ghostAgent):
    "Sets the ghost agent for later access"
    self.ghostAgent = ghostAgent
    self.index = ghostAgent.index
    
  def getPositionDistribution(self, gameState):
    """
    Returns a distribution over successor positions of the ghost from the given gameState.
    
    You must first place the ghost in the gameState, using setGhostPosition below.
    """
    ghostPosition = gameState.getGhostPosition(self.index) # The position you set
    actionDist = self.ghostAgent.getDistribution(gameState)
    dist = util.Counter()
    for action, prob in actionDist.items():
      successorPosition = game.Actions.getSuccessor(ghostPosition, action)
      dist[successorPosition] = prob
    return dist
  
  def setGhostPosition(self, gameState, ghostPosition):
    """
    Sets the position of the ghost for this inference module to the specified
    position in the supplied gameState.
    """
    conf = game.Configuration(ghostPosition, game.Directions.STOP)
    gameState.data.agentStates[self.index] = game.AgentState(conf, False)
    return gameState
  
  def observeState(self, gameState):
    "Collects the relevant noisy distance observation and pass it along."
    distances = gameState.getNoisyGhostDistances()
    if len(distances) >= self.index: # Check for missing observations
      obs = distances[self.index - 1]
      self.observe(obs, gameState)
      
  def initialize(self, gameState):
    "Initializes beliefs to a uniform distribution over all positions."
    # The legal positions do not include the ghost prison cells in the bottom left.
    self.legalPositions = [p for p in gameState.getWalls().asList(False) if p[1] > 1]   
    self.initializeUniformly(gameState)
    
  ######################################
  # Methods that need to be overridden #
  ######################################
  
  def initializeUniformly(self, gameState):
    "Sets the belief state to a uniform prior belief over all positions."
    pass
  
  def observe(self, observation, gameState):
    "Updates beliefs based on the given distance observation and gameState."
    pass
  
  def elapseTime(self, gameState):
    "Updates beliefs for a time step elapsing from a gameState."
    pass
    
  def getBeliefDistribution(self):
    """
    Returns the agent's current belief state, a distribution over
    ghost locations conditioned on all evidence so far.
    """
    pass

class ExactInference(InferenceModule):
  """
  The exact dynamic inference module should use forward-algorithm
  updates to compute the exact belief function at each time step.
  """
  
  def initializeUniformly(self, gameState):
    "Begin with a uniform distribution over ghost positions."
    self.beliefs = util.Counter()
    for p in self.legalPositions: self.beliefs[p] = 1.0
    self.beliefs.normalize()
  
  def observe(self, observation, gameState):
    """
    Updates beliefs based on the distance observation and Pacman's position.
    
    The noisyDistance is the estimated manhattan distance to the ghost you are tracking.
    
    The emissionModel below stores the probability of the noisyDistance for any true 
    distance you supply.  That is, it stores P(noisyDistance | TrueDistance).
    """
    noisyDistance = observation
    emissionModel = busters.getObservationDistribution(noisyDistance)
    pacmanPosition = gameState.getPacmanPosition()
    
    "*** YOUR CODE HERE ***"
    
    #their old code
    """
    # Replace this code with a correct observation update
    allPossible = util.Counter()
    for p in self.legalPositions:
      trueDistance = util.manhattanDistance(p, pacmanPosition)
      if emissionModel[trueDistance] > 0: allPossible[p] = 1.0
    allPossible.normalize()
    
        
    "*** YOUR CODE HERE ***"
    self.beliefs = allPossible
    """
    
    #OUR CODE HERE
    #lyee's attempt at code!
    
    allPossible = util.Counter()
    for p in self.legalPositions:
      trueDistance = util.manhattanDistance(p, pacmanPosition)
      if emissionModel[trueDistance] > 0:
        #noisy dist is the est manhattan dist to the ghost
        if noisyDistance == None:
          allPossible[p] = 1.0
        else:
          allPossible[p] = emissionModel[trueDistance] * self.beliefs[p]
    allPossible.normalize()
    self.beliefs = allPossible
    #END OUR CODE HERE
    
  def elapseTime(self, gameState):
    """
    Update self.beliefs in response to a time step passing from the current state.
    
    The transition model is not entirely stationary: it may depend on Pacman's
    current position (e.g., for DirectionalGhost).  
    
    You will need to use two helper methods provided in InferenceModule above:
      1) self.setGhostPosition(gameState, ghostPosition)
          This method alters the gameState by placing the ghost we're tracking
          in a particular position.  This altered gameState can be used to query
          what the ghost would do in this position.
      
      2) self.getPositionDistribution(gameState)
          This method uses the ghost agent to determine what positions the ghost
          will move to from the provided gameState.  The ghost must be placed
          in the gameState with a call to self.setGhostPosition above.
    """
    
    "*** YOUR CODE HERE ***"
    #OUR CODE HERE

    ct = util.Counter()

    #go through all pos
    for position in self.legalPositions:
      #get the position distr for the position (by plaing the ghost there and quereying via the setGhostPosition)
      #NOTE: not sure if we need to set the ghost back to it's original position... but idk how to get the rorignal positon of the ghost
      newPositionDistribution = self.getPositionDistribution(self.setGhostPosition(gameState, position))
      #update for each
      for newPosition, probability in newPositionDistribution.items():
        #exp val
        ct[newPosition] += probability * self.beliefs[position]
    #update beliefs
    self.beliefs = ct
    # END OUR CODE

  def getBeliefDistribution(self):
    return self.beliefs

class ParticleFilter(InferenceModule):
  """
  A particle filter for approximately tracking a single ghost.
  
  Useful helper functions will include random.choice, which chooses
  an element from a list uniformly at random, and util.sample, which
  samples a key from a Counter by treating its values as probabilities.
  """
  
  def initializeUniformly(self, gameState, numParticles=300):
    "Initializes a list of particles."
    self.numParticles = numParticles
    "*** YOUR CODE HERE ***"
    self.beliefs = util.Counter()
    for i in range(self.numParticles): self.beliefs[random.choice(self.legalPositions)] += 1

  def observe(self, observation, gameState):
    "Update beliefs based on the given distance observation."
    emissionModel = busters.getObservationDistribution(observation)
    pacmanPosition = gameState.getPacmanPosition()
    "*** YOUR CODE HERE ***"
    weights = util.Counter()
    for pos in self.beliefs:
      weights[pos]=self.beliefs[pos]*emissionModel[util.manhattanDistance(pacmanPosition,pos)]
    temp = util.Counter()
    if weights.totalCount()==0:
      self.initializeUniformly(gameState,self.numParticles)
      return None

    for i in range(self.numParticles):
      sample = util.sample(weights)
      temp[sample]+=1
    self.beliefs=temp

  def elapseTime(self, gameState):
    "Update beliefs for a time step elapsing."
    "*** YOUR CODE HERE ***"
    temp = util.Counter()
    #print 'len of self.beliefs at the start of elapse time ',len(self.beliefs.keys())
    #print 'number of particles: ',self.numParticles
    for pos in self.beliefs.keys():

      #if self.beliefs[pos]==0: continue
            #print 'Ghost position ',pos
      #print 'Position distribution ', self.getPositionDistribution(gameState)
      #import time
      #print 'position ', pos
      state = self.setGhostPosition(gameState,pos)

      #if not pos in self.legalPositions:
        #print 'the position is not a legal position!! KERNEL PANIC'
        #time.sleep(20)

      #if self.getPositionDistribution
      #if state is None:
        #print 'state was none'
          
      #import time 
      #if len(self.getPositionDistribution(state)) is 0: 
        #print 'the class of state is ', state.__class__.__name__
        #print 'position distribution ', self.getPositionDistribution(state)
        #time.sleep(10000000)
      #print self.beliefs[pos]
      for i in range(self.beliefs[pos]):
        newSample = util.sample(self.getPositionDistribution(state))
        temp[newSample]+=1
    self.beliefs=temp
    #print 'after elapse time ends, the length of self.beliefs is : ', len(self.beliefs.keys())
    
    #time.sleep(20)





  def getBeliefDistribution(self):
    """
    Return the agent's current belief state, a distribution over
    ghost locations conditioned on all evidence and time passage.
    """
    "*** YOUR CODE HERE ***"
    import copy
    return copy.deepcopy(self.beliefs)

class MarginalInference(InferenceModule):
  "A wrapper around the JointInference module that returns marginal beliefs about ghosts."

  def initializeUniformly(self, gameState):
    "Set the belief state to an initial, prior value."
    if self.index == 1: jointInference.initialize(gameState, self.legalPositions)
    jointInference.addGhostAgent(self.ghostAgent)
    
  def observeState(self, gameState):
    "Update beliefs based on the given distance observation and gameState."
    if self.index == 1: jointInference.observeState(gameState)
    
  def elapseTime(self, gameState):
    "Update beliefs for a time step elapsing from a gameState."
    if self.index == 1: jointInference.elapseTime(gameState)
    
  def getBeliefDistribution(self):
    "Returns the marginal belief over a particular ghost by summing out the others."
    jointDistribution = jointInference.getBeliefDistribution()
    dist = util.Counter()
    for t, prob in jointDistribution.items():
      dist[t[self.index - 1]] += prob
    return dist
  
class JointParticleFilter:
  "JointParticleFilter tracks a joint distribution over tuples of all ghost positions."
  
  def initialize(self, gameState, legalPositions, numParticles = 600):
    "Stores information about the game, then initializes particles."
    self.numGhosts = gameState.getNumAgents() - 1
    self.numParticles = numParticles
    self.ghostAgents = []
    self.legalPositions = legalPositions
    self.initializeParticles()
    
  def initializeParticles(self):
    "Initializes particles randomly.  Each particle is a tuple of ghost positions."
    self.particles = []
    for i in range(self.numParticles):
      self.particles.append(tuple([random.choice(self.legalPositions) for j in range(self.numGhosts)]))

  def addGhostAgent(self, agent):
    "Each ghost agent is registered separately and stored (in case they are different)."
    self.ghostAgents.append(agent)
    
  def elapseTime(self, gameState):
    """
    Samples each particle's next state based on its current state and the gameState.
    
    You will need to use two helper methods provided below:
      1) setGhostPositions(gameState, ghostPositions)
          This method alters the gameState by placing the ghosts in the supplied positions.
      
      2) getPositionDistributionForGhost(gameState, ghostIndex, agent)
          This method uses the supplied ghost agent to determine what positions 
          a ghost (ghostIndex) controlled by a particular agent (ghostAgent) 
          will move to in the supplied gameState.  All ghosts
          must first be placed in the gameState using setGhostPositions above.
          Remember: ghosts start at index 1 (Pacman is agent 0).  
          
          The ghost agent you are meant to supply is self.ghostAgents[ghostIndex-1],
          but in this project all ghost agents are always the same.
    """
    #print gameState
    newParticles = []
    for oldParticle in self.particles:
      newParticle = list(oldParticle) # A list of ghost positions
      "*** YOUR CODE HERE ***"
      state = setGhostPositions(gameState,newParticle)
      for i in range(len(newParticle)):
        newParticle[i]=util.sample(getPositionDistributionForGhost(state,i+1,self.ghostAgents[i]))
      newParticles.append(tuple(newParticle))
    self.particles=newParticles


    """
    temp = []
    #print 'len of self.beliefs at the start of elapse time ',len(self.beliefs.keys())
    #print 'number of particles: ',self.numParticles
    for vector in self.particles:

      #if self.beliefs[pos]==0: continue
            #print 'Ghost position ',pos
      #print 'Position distribution ', self.getPositionDistribution(gameState)
      #import time
      #print 'position ', pos
      state = setGhostPositions(gameState,vector)

      #if not pos in self.legalPositions:
        #print 'the position is not a legal position!! KERNEL PANIC'
        #time.sleep(20)

      #if self.getPositionDistribution
      #if state is None:
        #print 'state was none'
          
      #import time 
      #if len(self.getPositionDistribution(state)) is 0: 
        #print 'the class of state is ', state.__class__.__name__
        #print 'position distribution ', self.getPositionDistribution(state)
        #time.sleep(10000000)
      #print self.beliefs[pos]
      for gn in range(1,self.gameState.getNumAgents()):

          newSample = util.sample(self.getPositionDistributionForGhost(state, gn, self.ghostAgents[gn-1]))
          temp.append(newSample)
    self.particles = temp
    #print 'after elapse time ends, the length of self.beliefs is : ', len(self.beliefs.keys())
    
    #time.sleep(20)
"""


  
  def observeState(self, gameState):
    """
    Resamples the set of particles using the likelihood of the noisy observations.
    
    A correct implementation will handle two special cases:
      1) When a ghost is captured by Pacman, all particles should be updated so
          that the ghost appears in its cell, position (2 * ghostIndex - 1, 1).
          Captured ghosts always have a noisyDistance of 999.
         
      2) When all particles receive 0 weight, they should be recreated from the
          prior distribution by calling initializeParticles.  
    """ 
    pacmanPosition = gameState.getPacmanPosition()
    noisyDistances = gameState.getNoisyGhostDistances()
    if len(noisyDistances) < self.numGhosts: return
    emissionModels = [busters.getObservationDistribution(dist) for dist in noisyDistances]

    "*** YOUR CODE HERE ***"
    
    """
    def observe(self, observation, gameState):
    emissionModel = busters.getObservationDistribution(observation)
    pacmanPosition = gameState.getPacmanPosition()
    weights = util.Counter()
    for pos in self.beliefs:
      weights[pos] = self.beliefs[pos]*emissionModel[util.manhattanDistance(pacmanPosition,pos)]
    temp = util.Counter()
    if weights.totalCount()==0:
      self.initializeUniformly(gameState,self.numParticles)
      return None

    for i in range(self.numParticles):
      sample = util.sample(weights)
      temp[sample]+=1
    self.beliefs=temp
    """
    
    "*** YOUR CODE HERE ***"
    weights = util.Counter()
    for particle in self.particles:
      avg = 0
      for ghostNum in range(0, gameState.getNumAgents() - 1):
        avg += emissionModels[ghostNum][util.manhattanDistance(pacmanPosition, particle[ghostNum])]
      weights[particle] = avg / (gameState.getNumAgents() - 1)
    temp = []
    if weights.totalCount() is 0:
      self.initializeUniformly(gameState, self.numParticles)
      return None

    for i in range(self.numParticles):
      sample = util.sample(weights)
      temp.append(sample)
    self.particles = temp

  
  def getBeliefDistribution(self):
    dist = util.Counter()
    for part in self.particles: dist[part] += 1
    dist.normalize()
    return dist

# One JointInference module is shared globally across instances of MarginalInference 
jointInference = JointParticleFilter()

def getPositionDistributionForGhost(gameState, ghostIndex, agent):
  """
  Returns the distribution over positions for a ghost, using the supplied gameState.
  """
  ghostPosition = gameState.getGhostPosition(ghostIndex) 
  actionDist = agent.getDistribution(gameState)
  dist = util.Counter()
  for action, prob in actionDist.items():
    successorPosition = game.Actions.getSuccessor(ghostPosition, action)
    dist[successorPosition] = prob
  return dist
  
def setGhostPositions(gameState, ghostPositions):
  "Sets the position of all ghosts to the values in ghostPositionTuple."
  for index, pos in enumerate(ghostPositions):
    conf = game.Configuration(pos, game.Directions.STOP)
    gameState.data.agentStates[index + 1] = game.AgentState(conf, False)
  return gameState  

