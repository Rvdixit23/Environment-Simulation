import numpy as np
import matplotlib.pyplot as plt
import random
import math


def gauss_random(mean=0, variance=13 / 45):
    """
    Wrapper function for generating random numbers of the desired distribution
    Parameters : mean, variance
    Returns : Random number sampled from Gaussian Distribution
    """
    return abs(1 - abs(random.gauss(mean, variance)))


# def exp_random():
#     return np.random.gamma(1, 2.0)


def generate_qualdict(qualities, chance):
    qualities = sorted(qualities, key=lambda x: np.array(x).dot(chance))
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


def mutator(val, qualities_dict, chance, mutate_percent):
    if (random.random() < (mutate_percent / 100)):
        chance_value = np.array(qualities_dict[val]).dot(chance)
        # new_val = val
        # while (new_val < max(qualities_dict.keys())
        #        and chance_value >= np.array(qualities_dict[val]).dot(chance)):
        #     new_val += 1
        return random.randint(max([1, val]),
                              min([max(qualities_dict.keys()), val + 3]))
    else:
        return val


f = 3  # number of features
n = 300  # initial number of beings
per = 10  # lower percentage of population
mutate_per = 5  # chance to mutate to an advanced specie
epochs = 1000  # number of generations
food_lower = 180  # least amount of food
food_higher = 360  # most amount of food
types_of_beings = 50  # max types of beings

qualities = []
while (len(qualities) != types_of_beings):
    ele = [random.randint(2, 8) for i in range(f)]
    if (ele not in qualities):
        qualities.append(ele)

chance = np.reshape([random.randint(3, 6) for i in range(f)], (f, 1))
qualities_dict = generate_qualdict(qualities, chance)
populist = init_population_generate(qualities_dict, n, per)
init_popul_dict = dict((i, populist.count(i))
                       for i in range(1, types_of_beings + 1)
                       if populist.count(i))

print(chance)
print(qualities_dict)
print("\n\n")
print("initial_beings")
print(populist)
print("\n\n")

food_list = [random.randint(food_lower, food_higher)
             for i in range(epochs)]  # resource available for each generation

for i in range(epochs):  # number of epochs (generations)
    if (not int(i % 10)):
        print("running epoch_set:", i)
        print(sorted(populist))
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
            mutator(new_birth, qualities_dict, chance, mutate_per))
    populist = new_populist

final_popul_dict = dict((i, populist.count(i))
                        for i in range(1, types_of_beings + 1)
                        if populist.count(i))
print("init_dict")
print(init_popul_dict)
print("final_dict")
print(final_popul_dict)
