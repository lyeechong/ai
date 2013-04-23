import util
import classificationMethod

class contestClassifier(classificationMethod.ClassificationMethod):
  """
  Create any sort of classifier you want. You might copy over one of your
  existing classifiers and improve it.
  """
  def __init__(self, legalLabels):
    self.guess = None
    self.type = "minicontest"
  
  def train(self, data, labels, validationData, validationLabels):
    """
    Please describe your training procedure here.
    """
    
    # -- calls the classify method to evaluate performance    
    # -- OUR CODE HERE
    
    legalLabels = labels
    self.legalLabels = legalLabels
    trainingData = validationData
    trainingLabels = validationLabels
    
    kCorrect = util.Counter()
    self.conditionalProb = []
    
    
    self.prior = util.Counter()
    for label in labels:
      self.prior[label] += 1.0
    self.prior.normalize()
    #for label in self.prior:
    #  self.prior[label]/=len(trainingLabels)
    
    """
    print "legal labels are ", len(legalLabels)
    print "kgrid is ", kgrid
    print "the legal labels are.... ", legalLabels
    """
    
    import time
    
    condprobForK = {}
    
    # -- iterate through each k in kgrid... should we be doing this?
    # -- won't this affect the cond prob tables? :(
    k = 0.5
    #print "working on k = ",k," in kgrid"
    
    # -- reset the conditonal prob table
    # -- each time we go through a different k...
    self.conditionalProb = {}
    
    # -- go through each label and initialize the Counter for that label (the cond prob table)
    for label in legalLabels:
      self.conditionalProb[label] = util.Counter()
      
    # -- go through each piece of training data and train the tables on it  
    for dataNum in range(len(trainingData)):
    
      # -- identify which label we're using... not sure if this is correct
      label = trainingLabels[dataNum] # 0 or like 9 or 2
      
      # -- iterate through each pixel and update the conditional prob counter for that label
      for pixel in trainingData[dataNum]:
        
        if pixel is "moreThanOneConnBlackRegions":
          #print "Number is :: ", label, " and has ", trainingData[dataNum][pixel]
          assert 1 is 1
        
        on_off = trainingData[dataNum][pixel] * 1.0
        self.conditionalProb[label][pixel] += on_off * 1.0
        
    # -- now we go through and add k to each of the conditional probabilities
    # -- note that we do so for each label and every single pixel
    for label in legalLabels:
      for pixel in self.conditionalProb[label]:     
        # -- add the k value     
        self.conditionalProb[label][pixel] += k * 1.0
        assert self.conditionalProb[label][pixel] >= k # -- sanity check that it should be at least k
        self.conditionalProb[label][pixel] /= (self.prior[label] * len(trainingLabels) + k*2)
        
    
       
    # -- END OUR CODE
    
  def classify(self, testData):
    """
    Please describe how data is classified here.
    """
    guesses = []
    self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
    for datum in testData:
      posterior = self.calculateLogJointProbabilities(datum)
      guesses.append(posterior.argMax())
      self.posteriors.append(posterior)
    return guesses
    
  def calculateLogJointProbabilities(self, datum):
    """
    Returns the log-joint distribution over legal labels and the datum.
    Each log-probability should be stored in the log-joint counter, e.g.    
    logJoint[3] = <Estimate of log( P(Label = 3, datum) )>
    """
    logJoint = util.Counter()
    
    "*** YOUR CODE HERE ***"
    
    # -- OUR CODE HERE
    
    
    import math
    for label in self.legalLabels:
      sumThing = 0.0
      for pixel in self.conditionalProb[label]:
        if datum[pixel] is 1:
          #assert self.conditionalProb[label][pixel] < 1.0 # -- sanity check that the probability is valid
          sumThing += math.log((self.conditionalProb[label][pixel]*1.0))
        else:
          sumThing+=math.log(1-self.conditionalProb[label][pixel]*1.0)
      logJoint[label] = math.log(self.prior[label]*1.0) + sumThing*1.0
      

    
    
    import time
    #print "logJoint is :: ", logJoint
    #time.sleep(2)
    
    
    # -- uses the conditional probability tables computed in the current iteration
    # -- in train and tune
    
    return logJoint
