# qlearningAgents.py
# ------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math
          
class QLearningAgent(ReinforcementAgent):
  """
    Q-Learning Agent
    
    Functions you should fill in:
      - getQValue
      - getAction
      - getValue
      - getPolicy
      - update
      
    Instance variables you have access to
      - self.epsilon (exploration prob)
      - self.alpha (learning rate)
      - self.gamma (discount rate)
    
    Functions you should use
      - self.getLegalActions(state) 
        which returns legal actions
        for a state
  """
  def __init__(self, **args):
    "You can initialize Q-values here..."
    ReinforcementAgent.__init__(self, **args)

    "*** YOUR CODE HERE ***"
    #OUR CODE HERE
    #So I guess we need to make a counter to stick Q values in
    #Everything in it will be 0 because it's a counter
    self.qvalues = util.Counter()
    #woohoo! counters!
    
  
  def getQValue(self, state, action):
    """
      Returns Q(state,action)    
      Should return 0.0 if we never seen
      a state or (state,action) tuple 
    """
    "*** YOUR CODE HERE ***"
    #OUR CODE HERE
    #note to kendall: added a quick if check to see if it has been seen
    #since it says so in the comments above
    if (state, action) in self.qvalues:
      return self.qvalues[(state,action)]
    else:
      return 0.0

  
    
  def getValue(self, state):
    """
      Returns max_action Q(state,action)        
      where the max is over legal actions.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return a value of 0.0.
    """
    "*** YOUR CODE HERE ***"
    #OUR CODE HERE

    #Okay, so in the instructions it has a hint that says we can't just
    #use argmax because the "actual argmax you want may be a key not in
    #the counter!". Not sure why that's the case or if it's relevant here
    
    maximum = -sys.maxint-1 #old kendall code
    #maximum = -float("inf") #new lyee code!
    #maximum = 0.0 #newerrrr lyee code
    if self.getLegalActions(state) == None or len(self.getLegalActions(state)) is 0:
      return 0.0
    for action in self.getLegalActions(state):
      maximum = max(maximum, self.qvalues[(state, action)])
    return maximum
    #lyee says: i think this code looks good

  def getPolicy(self, state):
    """
      Compute the best action to take in a state.  Note that if there
      are no legal actions, which is the case at the terminal state,
      you should return None.
    """
    "*** YOUR CODE HERE ***"
    #OUR CODE HERE
    
    #Again, the argmax warning scares me, so I just avoid argmax...

    maximum = -sys.maxint-1 #old kendall code
    #maximum = -float("inf") #new lyee code!
    if self.getLegalActions(state)==None or len(self.getLegalActions(state)) is 0:
      return None
    bestAction = []
    for action in self.getLegalActions(state):
      if self.qvalues[(state,action)]==maximum: #Lyee fix: I think you meant self.qvalues instead of qvalue
        #If there's a tie, apparently we choose the best action randomly
        bestAction.append(action)# = random.choice((bestAction, action)) #lyee fix: changed it into a tuple instead of 2 args
      elif self.qvalues[(state,action)]>maximum:#Lyee fix: I think you meant self.qvalues instead of qvalue
        maximum=self.qvalues[(state,action)]#Lyee fix: I think you meant self.qvalues instead of qvalue
        bestAction = [action]
    return random.choice(bestAction)
    #lyee says: ehhh looks okay I suppose!
    #mmm... side note thought: wouldn't the best action just be the action
    #with the q-value returned from when we do self.getValue(state) then we
    #can easily check if the action has that value, it's the best action?
    

    
  def getAction(self, state):
    """
      Compute the action to take in the current state.  With
      probability self.epsilon, we should take a random action and
      take the best policy action otherwise.  Note that if there are
      no legal actions, which is the case at the terminal state, you
      should choose None as the action.
    
      HINT: You might want to use util.flipCoin(prob)
      HINT: To pick randomly from a list, use random.choice(list)
    """  
    # Pick Action
    legalActions = self.getLegalActions(state)
    action = None
    "*** YOUR CODE HERE ***"
    #OUR CODE HERE

    if legalActions==None or len(legalActions) is 0:
        return None

    #So do we take a random action or not?
    if util.flipCoin(self.epsilon): #lyee says: no idea what epsilon is!
      #We will take a random action
      action= random.choice(legalActions)
    else:
      #We follow the policy
      action = self.getPolicy(state) #lyee fix: kendall previously had just getPolicy.. I added the 'self' part. hope that's what kendall meant D:
    return action
  
  def update(self, state, action, nextState, reward):
    """
      The parent class calls this to observe a 
      state = action => nextState and reward transition.
      You should do your Q-Value update here
      
      NOTE: You should never call this function,
      it will be called on your behalf
    """
    "*** YOUR CODE HERE ***"
    #We update the Q value. Straight from page 844 of the book. Not sure if I did R(s) or maxQ(s',a') correctly
    
    #lyee says: the pdf book code is a bit missing, so I whipped out my physical 2nd ed. copy
    #and somewhat rewrote the equation
    # Equation is:
    # Q[a, s] = Q[a, s] + alpha * (N[s, a]) * (r + gamma * Q[a', s'] - Q[a, s])
    
    Q = self.qvalues[(state, action)]
    a = self.alpha
    y = self.gamma
    r = reward
    n = self.getValue(nextState)
    self.qvalues[(state, action)] = Q+a*(r+y*n-Q) #btw, left out N[s, a] from the equation...
    
    #below here, lies old Kendall code
    #RIP until needed
    """
    self.qvalues[(state,action)] = \
    self.qvalues[(state,action)] + \
    self.alpha * (self.getValue(state) + \ #old kendall code
    self.gamma * self.getValue(nextState) - \
    self.qvalues[(state,action)])
    """
    
class PacmanQAgent(QLearningAgent):
  "Exactly the same as QLearningAgent, but with different default parameters"
  
  def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
    """
    These default parameters can be changed from the pacman.py command line.
    For example, to change the exploration rate, try:
        python pacman.py -p PacmanQLearningAgent -a epsilon=0.1
    
    alpha    - learning rate
    epsilon  - exploration rate
    gamma    - discount factor
    numTraining - number of training episodes, i.e. no learning after these many episodes
    """
    args['epsilon'] = epsilon
    args['gamma'] = gamma
    args['alpha'] = alpha
    args['numTraining'] = numTraining
    self.index = 0  # This is always Pacman
    QLearningAgent.__init__(self, **args)

  def getAction(self, state):
    """
    Simply calls the getAction method of QLearningAgent and then
    informs parent of action for Pacman.  Do not change or remove this
    method.
    """
    action = QLearningAgent.getAction(self,state)
    self.doAction(state,action)
    return action

    
class ApproximateQAgent(PacmanQAgent):
  """
     ApproximateQLearningAgent
     
     You should only have to overwrite getQValue
     and update.  All other QLearningAgent functions
     should work as is.
  """
  def __init__(self, extractor='IdentityExtractor', **args):
    self.featExtractor = util.lookup(extractor, globals())()
    PacmanQAgent.__init__(self, **args)

    # You might want to initialize weights here.
    "*** YOUR CODE HERE ***"
    
  def getQValue(self, state, action):
    """
      Should return Q(state,action) = w * featureVector
      where * is the dotProduct operator
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()
    
  def update(self, state, action, nextState, reward):
    """
       Should update your weights based on transition  
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()
    
  def final(self, state):
    "Called at the end of each game."
    # call the super-class final method
    PacmanQAgent.final(self, state)
    
    # did we finish training?
    if self.episodesSoFar == self.numTraining:
      # you might want to print your weights here for debugging
      "*** YOUR CODE HERE ***"
      pass
