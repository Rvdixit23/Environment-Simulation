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

class Being(BeingBase):
    # Being.chance = chance
    def __init__(self, featureValueList):
        super().__init__(featureValueList)
    
    def endOfDayResult(self, food):
        if food == 2:
            return self.reproduce()
        elif food == 1:
            return 1
        else:
            return 0
        
    def reproduce(self):
        
        

    

    
