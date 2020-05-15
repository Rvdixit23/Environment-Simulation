from matplotlib import pyplot
from copy import deepcopy
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
        self.features = np.array(featureValueList)
        self.speed = featureValueList[0]
        self.intelligence = featureValueList[1]
        self.age = 0
        self.food = 0

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
    

    def endOfDayResult(self, environment):
        """
        Returns the action of the being
        At the end of the day depending on the food
        It had collected on that day
        """
        self.age += 1
        if self.food == 2:
            self.food = 0
            return [self, self.reproduce(\
                environment.mutationChance, environment.qualityMultiplier)]
        elif self.food == 1:
            self.food = 0
            return [self]
        else:
            self.food = 0
            return 0
        
    def reproduce(self, mutChance, qualityMultiplier, chance):
        """
        Reproduces a mutated being with a large chance of
        Increase in capability
        Chance of mutation is given by mutationChance
        Return : Being
        """
        if random.random() < mutationChance:
            indexOfFeature = random.choice([0, 1])
            tempList = list(self.features)
            newBeing = Being(tempList)
            newBeing.features[indexOfFeature] *= qualityMultiplier
            newBeing.survivalChance = newBeing.features.dot(chance)
            return newBeing
        else:
            newBeing = Being(self.features)
            newBeing.survivalChance = self.survivalChance
            return newBeing
    

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
        self.foodCountMean = foodCountMean
        self.foodCountVariance = foodCountVariance
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
                newBeing.survivalChance = newBeing.features.dot(self.chance)
                self.population.append(newBeing)
        elif featureValues:
            for i in range(startingPopulation):
                newBeing = Being(featureValues[i])
                newBeing.survivalChance = newBeing.features.dot(self.chance)
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
        todayFood = self.generateFoodCount(self.foodCountMean, \
            self.foodCountVariance)
        todayFood = round(todayFood)
        self.population = sorted(self.population, \
            key=lambda being : being.survivalChance, reverse=True)



        maxChance = self.population[0].survivalChance
        minChance = self.population[-1].survivalChance
        newPopulation = list()
        acquisitionIndex = 0
        self.count = len(self.population)
        if maxChance - minChance > 1:    
            print("Percentile grade")
            for being in self.population:
                being.relativeProb = (being.survivalChance - minChance)/(maxChance - minChance)
        else:
            print("Random Grade")
            for i in range(self.count):
                self.population[i].relativeProb = i/self.count

        while todayFood > 0:
            # print(self.population[acquisitionIndex].relativeProb \
            #     < type2simulation.gauss_random())
            if self.population[acquisitionIndex].relativeProb \
                < type2simulation.gauss_random():
                self.population[acquisitionIndex].food += 1
                acquisitionIndex = (acquisitionIndex + 1) % self.count
                todayFood -= 1
                # print(todayFood)
        
        
        
        
        for being in self.population:
            # print(being.food)
            if being.food >= 2:
                newPopulation.append(being)
                newPopulation.append(being.reproduce(self.mutationChance, \
                    self.qualityMultiplier, self.chance))
            elif being.food == 1:
                newPopulation.append(being)
            being.food = 0

        # print(newPopulation)
        self.population = deepcopy(newPopulation)

        

    def runSimulation(self, numberOfDays):
        dataList = list()
        for day in range(numberOfDays):
            if any(self.population):
                self.runDay()
            else:
                break
            print("Day : {}".format(day + 1))
            dataList.append(self.count)
        print(dataList)
        pyplot.plot(dataList)
        pyplot.show()

if __name__ == "__main__":
    envConfig = {
        "mutationChance" : 0.05, 
        "qualityMultiplier" : 1.5,
        "foodCountMean" : 100, 
        "chanceList" : [0.3, 0.6]
    }
    env = Environment(**envConfig)
    populationConfig = {
        "startingPopulation" : 30,
        "featureValues" : [[i, i] for i in range(30)]
    }
    print("Creating population ....")
    env.createPopulation(**populationConfig)
    print("Running simulation ....")
    env.runSimulation(200)

            
        
    
