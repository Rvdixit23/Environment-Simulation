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
        self.age = 0

    def __str__(self):
        return "Speed : {}\nIntelligence : {}".format(\
            self.speed, self.intelligence)

# chance = np.array([0.2, 0.8])
# Weights for the increase in survival chance for 
# Speed and intelligence
mutationChance = 0.05
qualityMultiplier = 1.1
        
class Being(BeingBase):

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
            return 0
        
    def reproduce(self, mutChance, qualityMultiplier):
        """
        Reproduces a mutated being with a large chance of
        Increase in capability
        Chance of mutation is given by mutationChance
        Return : Being
        """
        if random.random() < mutationChance:
            indexOfFeature = random.choice([0, 1])
            tempList = list(self.features)
            self.features[indexOfFeature] *= qualityMultiplier
            return Being(tempList)
        else:
            return Being(self.features)
    

class Environment():

    def __init__(self, mutationChance, qualityMultiplier, \
        foodCountMean, chanceList, foodCountVariance=0):
        """
        Creates and environment for running a simulation in
        mutationChance : Probability of mutation
        qualityMultiplier : Increase in the feature after mutation
        foodCountMean : Mean of the food that spawns everyday
        chanceList : The G - Matrix, representing the weightage for
            each feature to survive
        
        Optional : foodCount Variance(Default : 0)
        Returns : None
        """
        self.mutationChance = mutationChance
        self.qualityMultiplier = qualityMultiplier
        self.generateFoodCount = lambda foodCountMean, foodCountVariance: \
            random.gauss(foodCountMean, foodCountVariance)
        # self.foodRetrievalChances = foodRetrievalChances
        self.chance = np.array(chanceList)

    def createPopulation(self, startingPopulation, \
        feature=None, featureValues=None):
        """
        Creates a population in the environment with the features
            given
        startingPopulation : Number of beings in the beginning of
            the simulation
        feature : A list if all beings have the same features
        featureValues : A list of lists with the features
            of each being, len(featureValues) = startingPopulation

        Returns : None
        """
        self.population = list()
        if not featureValues:
            for i in range(startingPopulation):
                newBeing = Being(feature)
                newBeing.survivalProb = newBeing.features.dot(self.chance)
                self.population.append(newBeing)
        elif featureValues:
            for i in range(startingPopulation):
                newBeing = Being(featureValues[i])
                newBeing.survivalProb = newBeing.features.dot(self.chance)
                self.population.append(newBeing)
        else:
            raise Exception("Wrong input parameter")

    def runDay(self):
        """
        Runs a day in the simulation
        Generates food for the day
        Each being gets either 0, 1, or 2 food
        Beings which get 0 die
        """
        todayFood = self.generateFoodCount()
        self.population = sorted(self.population, \
            key=lambda being : being.survivalProb)
        # Decide how 0, 1 or 2 food is obtained by one being
        # Calculate survivors here


            


    def runSimulation(self, numberOfDays):
        for day in range(numberOfDays):
            self.runDay()
    

if __name__ == "__main__":
    a = list()
    for i in range(10000):
        a.append(type2simulation.gauss_random())
    pyplot.hist(a, bins = 50)
    pyplot.show()

            
        
    
