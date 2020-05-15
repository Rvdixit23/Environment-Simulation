from matplotlib import pyplot
import random
import math
import numpy as np
import type2simulation

#################################################
# In this program it is assumed that the first 
# feature is the speed and the second is intelligence
#################################################

class BeingBase(object):
    def __init__(self, featureValueList):
        """
        Creates a matrix to show the features of the being
        """
        self.features = np.array(*featureValueList)
        self.speed = featureValueList[0]
        self.intelligence = featureValueList[1]

    def __str__(self):
        return "Speed : {}\nIntelligence : {}".format(\
            self.speed, self.intelligence)

# chance = np.array([0.2, 0.8])
# Weights for the increase in survival chance for 
# Speed and intelligence
mutationChance = 0.05
qualityMultiplier = 1.1

def setClassParams(mutationChance, qualityMultiplier):
        Being.mutationChance = mutationChance
        Being.qualityMultiplier = qualityMultiplier
        
class Being(BeingBase):
    
    setClassParams()

    def __init__(self, featureValueList):
        super().__init__(featureValueList)
    

    def endOfDayResult(self, food):
        """
        Returns the action of the being
        At the end of the day depending on the food
        It had collected on that day
        """
        if food == 2:
            return self.reproduce()
        elif food == 1:
            return 1
        else:
            return 0
        
    def reproduce(self):
        """
        Reproduces a mutated being with a large chance of
        Increase in capability
        Chance of mutation is given by mutationChance
        Return : Being
        """
        if random.random() < Being.mutationChance:
            indexOfFeature = random.choice([0, 1])
            tempList = list(self.features)
            self.features[indexOfFeature] *= Being.qualityMultiplier
            return Being(tempList)
        else:
            return Being(self.features)
    



    
