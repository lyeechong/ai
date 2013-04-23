import util
import classificationMethod
import math

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
  """
  See the project description for the specifications of the Naive Bayes classifier.
  
  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """
  def __init__(self, legalLabels):
    self.legalLabels = legalLabels
    self.type = "naivebayes"
    self.k = 1 # this is the smoothing parameter, ** use it in your train method **
    self.automaticTuning = False # Look at this flag to decide whether to choose k automatically ** use this in your train method **
    
  def setSmoothing(self, k):
    """
    This is used by the main method to change the smoothing parameter before training.
    Do not modify this method.
    """
    self.k = k

  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Outside shell to call your method. Do not modify this method.
    """  
      
    self.features = trainingData[0].keys() # this could be useful for your code later...
    
    if (self.automaticTuning):
        kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50]
    else:
        kgrid = [self.k]
        
    self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)
      
  def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
    """
    Trains the classifier by collecting counts over the training data, and
    stores the Laplace smoothed estimates so that they can be used to classify.
    Evaluate each value of k in kgrid to choose the smoothing parameter 
    that gives the best accuracy on the held-out validationData.
    
    trainingData and validationData are lists of feature Counters.  The corresponding
    label lists contain the correct label for each datum.
    
    To get the list of all possible features or labels, use self.features and 
    self.legalLabels.
    """

    "*** YOUR CODE HERE ***"

    # -- calls the classify method to evaluate performance    
    # -- OUR CODE HERE
    
    features = self.features
    legalLabels = self.legalLabels
    
    kCorrect = util.Counter()
    self.conditionalProb = []
    
    
    self.prior = util.Counter()
    for label in trainingLabels:
      self.prior[label] += 1.0
    self.prior.normalize()
    
    """
    print "legal labels are ", len(legalLabels)
    print "kgrid is ", kgrid
    print "the legal labels are.... ", legalLabels
    """
    
    import time
    
    condprobForK = {}
    
    # -- iterate through each k in kgrid... should we be doing this?
    # -- won't this affect the cond prob tables? :(
    for k in kgrid:
      k = k * 1.0
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
          
      # !!!! -- debugging zone ahead!
      
      #self.printCondProbTableThing(self.conditionalProb[1])
      #time.sleep(30)
      
      # !!!! -- end debugging zone!
      
      
      # -- then we go through each of the conditional probability tables for the labels
      # -- and normalize them
      for label in legalLabels:
        self.conditionalProb[label].normalize()
        assert 1 is 1
              
      guesses = self.classify(validationData)


      #print "the guesses are :: "
      #print guesses
      #print "the actual answers :: "
      #print validationLabels
      #assert len(guesses) is len(validationLabels)
      #time.sleep(10)
      
      for labelNum in range(len(guesses)):
        if guesses[labelNum] is validationLabels[labelNum]:
          kCorrect[k] += 1 * 1.0
      
      condprobForK[k] = self.conditionalProb
      
    self.conditionalProb = condprobForK[kCorrect.argMax()]
        
       
    # -- END OUR CODE
    #util.raiseNotDefined()
  
  
  # -- this is Lyee's method to print out a conditonal probabilty table
  def printCondProbTableThing(self, table):
    """
    Lyee's method!
    """
    my_matrix = [[0 for i in range(28)] for j in range(28)]
    for pixel in table:
      col = pixel[0]
      row = pixel[1]
      heat = table[pixel]
      if heat > 3.0:
        heat = "#"
      else:
        heat = " "
      my_matrix[row][col] = heat
    
    import string
    max_lens = [max([len(str(r[i])) for r in my_matrix]) for i in range(len(my_matrix[0]))]
    print "\n".join(["".join([string.ljust(str(e), l + 2) for e, l in zip(r, max_lens)]) for r in my_matrix])

  
  def classify(self, testData):
    """
    Classify the data based on the posterior distribution over labels.
    
    You shouldn't modify this method.
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
          sumThing += math.log(self.conditionalProb[label][pixel]*1.0)
          
      logJoint[label] = math.log(self.prior[label]*1.0) + sumThing*1.0
      
    
    """
    # -- Lyee's random code which gets 46%
    chances = util.Counter()
    for label in self.legalLabels:
      for pixel in self.conditionalProb[label]:        
        if datum[pixel] is 1:
          chances[label] += self.conditionalProb[label][pixel]
    
    chances.normalize()    
    return chances
    """
    
    
    import time
    #print "logJoint is :: ", logJoint
    #time.sleep(2)
    
    
    # -- uses the conditional probability tables computed in the current iteration
    # -- in train and tune
    
    return logJoint
  
  def findHighOddsFeatures(self, label1, label2):
    """
    Returns the 100 best features for the odds ratio:
            P(feature=1 | label1)/P(feature=1 | label2) 
    """
    featuresOdds = []
        
    "*** YOUR CODE HERE ***"
    
    cpTable1 = self.conditionalProb[label1]
    cpTable2 = self.conditionalProb[label2]
    
    dictionaryOfPixelToOdds = {}
    
    for pixel in cpTable1:
      dictionaryOfPixelToOdds[pixel] = cpTable1[pixel] / cpTable2[pixel]
        
    featuresOdds = sorted(dictionaryOfPixelToOdds, key = dictionaryOfPixelToOdds.get, reverse = True)
    featuresOdds = featuresOdds[:100]
    
    return featuresOdds
    

    
      
