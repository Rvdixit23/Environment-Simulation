import numpy as np
import matplotlib
import random
import math


def gauss_random():
    return abs(1 - abs(random.gauss(0, 20/45)))

def exp_random():
    return np.random.exponential(0.5)

def food_lucky(arr,populist):
    minimum = 1000
    ind = -1
    while(ind==-1 or populist[ind]==0):
        val=gauss_random()
        for i in range(len(arr)):
            if (abs(arr[i] - val) < minimum):
                minimum = abs(arr[i] - val)
                ind = i
    return populist[ind]


qualities = {
    0: [0, 0, 0],
    1: [3, 3, 3],
    2: [3, 2, 4],
    3: [2, 4, 3],
    4: [2, 5, 5]
}
populindex = {0: 1, 1: 30, 2: 60, 3: 25, 4: 15}
food=[random.randint(45,60) for i in range(100)] #food available for each generation

populist = []
for i in qualities:
    for j in range(populindex[i]):
            populist.append(i)

for i in range(100): # number of epochs (generations)
    populmatrix = np.array([qualities[i] for i in populist])
    chance = np.matrix("0.2;0.4;0.3")
    result = populmatrix.dot(chance)
    result_norm = np.asarray(
        np.interp(result, (result.min(), result.max()), (0, 1))).reshape(-1)
    #print(result_norm)
    new_populist=[]
    for j in range(food[i]):
        new_populist.append(food_lucky(result_norm,populist))
    print(new_populist)
    populist=new_populist    