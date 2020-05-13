import numpy as np
import matplotlib
import random
import math


def gauss_random(mean = 0, variance = 13/45):
    """
    Wrapper function for generating random numbers of the desired distribution
    Parameters : mean, variance
    Returns : Random number sampled from Gaussian Distribution
    """
    return abs(1 - abs(random.gauss(mean, variance)))


def exp_random():
    return np.random.gamma(1, 2.0)


def generate_qualdict(qualities):
    qualities = sorted(qualities, key=lambda x: sum(x))
    qualities.insert(0, [0 for i in range(len(qualities[1]))])
    return dict(zip(range(len(qualities)), qualities))


def init_population_generate(qualities_dict, num, lower_percentage):
    max_key = int(max(qualities_dict.keys()) * lower_percentage / 100)
    populist = []
    for i in range(num):
        populist.append(random.randint(1, max_key))
    populist.insert(0, 0)
    return populist


def food_lucky(arr, populist):
    minimum = 10000
    ind = -1
    while (ind == -1 or populist[ind] == 0):
        val = gauss_random()
        for i in range(len(arr)):
            if (abs(arr[i] - val) < minimum):
                minimum = abs(arr[i] - val)
                ind = i
    return populist[ind]


def mutator(val, qualities_dict, chance, adapt_percent):
    if (random.random() < (adapt_percent / 100)):
        chance_value = np.array(qualities_dict[val]).dot(chance)
        new_val = val
        while (new_val < max(qualities_dict.keys())
               and chance_value >= np.array(qualities_dict[val]).dot(chance)):
            new_val += 1
        return new_val
    else:
        return val


f = 10  # number of features
n = 100  # initial number of beings
per = 50  # lower percentage of population
adapt_per = 25  # chance to mutate to an advanced specie
epochs = 200  # number of generations
food_lower = 80  # least amount of food
food_higher = 120  # most amount of food

qualities = list(
    set([tuple([random.randint(2, 8) for i in range(f)]) for i in range(50)]))
chance = np.reshape([random.randint(3, 6) / 10 for i in range(f)], (f, 1))
qualities_dict = generate_qualdict(qualities)
populist = init_population_generate(qualities_dict, n, per)

print(chance)
print(qualities_dict)
print("\n\n")
print("initial_beings")
print(populist)
print("\n\n")

food_list = [random.randint(food_lower, food_higher)
             for i in range(epochs)]  # resource available for each generation

for i in range(epochs):  # number of epochs (generations)
    if(not int(i % 100)):
        print("running epoch_set:", i)
        print(populist)
        print("\n\n")
    populmatrix = np.array([qualities_dict[i] for i in populist])
    result = populmatrix.dot(chance)
    result_norm = np.asarray(
        np.interp(result, (result.min(), result.max()), (0, 1))).reshape(-1)
    # print(result_norm)
    new_populist = [0]
    for j in range(food_list[i]):
        new_birth = food_lucky(result_norm, populist)
        new_populist.append(
            mutator(new_birth, qualities_dict, chance, adapt_per))
    populist = new_populist

print("final_beings")
print(populist)
