# %%
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import pylab as pylab
import random
import math
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# %%


def gauss_random(mean=0, variance=13 / 45):
    """
    Wrapper function for generating random numbers of the desired distribution
    Parameters : mean, variance
    Returns : Random number sampled from Gaussian Distribution
    """
    return abs(1 - abs(random.gauss(mean, variance)))


# def exp_random():
#     return np.random.gamma(1, 2.0)


def generate_qualdict(qualities, chance, ones_mat):
    """
    This function returns the dictionary of the different species
    Keys of the dictionary shows how good the species is
    Example : qualDict[0] is inferior to qualDict[10]
    Input : List of tuples containing the rating for each feature of the species
    Output : Dictionary as specified above
    """
    qualities = sorted(qualities,
                       key=lambda x: np.array(x).dot(chance).dot(ones_mat))
    qualities.insert(0, [0 for i in range(len(qualities[1]))])
    return dict(zip(range(len(qualities)), qualities))


def init_population_generate(qualities_dict, num, lower_percentage):
    """
    This creates a list of beings
    Each being is referred to by the species number as specified in qualities_dict
    num : Number of beings in the population
    lower_percentage : Percentage of population belonging to inferior species
    Returns : List with species number for num beings
    """
    max_key = int(max(qualities_dict.keys()) * lower_percentage / 100)
    populist = []
    for i in range(num):
        populist.append(random.randint(1, max_key))
    populist.insert(0, 0)
    return populist


def food_lucky(arr, populist):
    """
    This function controls mutation within species
    val : Original species index
    qualities_dict : The species data
    chance : The probability of survival
    adapt_percent : The probability of mutation
    Returns : The new species index of the original species
    """
    minimum = 10000
    ind = -1
    while (ind == -1 or populist[ind] == 0):
        val = gauss_random()
        for i in range(len(arr)):
            if (abs(arr[i] - val) < minimum):
                minimum = abs(arr[i] - val)
                ind = i
    return populist[ind]


def mutator(val, qualities_dict, chance, mutate_percent, ones_mat):
    if (random.random() < (mutate_percent / 100)):
        chance_value = np.array(qualities_dict[val]).dot(chance).dot(ones_mat)
        # new_val = val
        # while (new_val < max(qualities_dict.keys())
        #        and chance_value >= np.array(qualities_dict[val]).dot(chance)):
        #     new_val += 1
        return random.randint(max([1, val]),
                              min([max(qualities_dict.keys()), val + 3]))
    else:
        return val


def generate_chance(f, maind_low, maind_high, rel_low, rel_high):
    """
    generates the conditional matrix of the given world on its impacts
    on the beings of the system on each feature
    main-dependency-low to main-dependency-high are the diagonal elements
    which have greater impact on the corresponding feature
    relative-dependency-low to relative-dependency-high are the side effects
    an environment condition on other features
    """
    chance = np.diag(np.ones(f))
    for i in range(f):
        for j in range(f):
            if (chance[i, j]):
                chance[i, j] = random.randint(maind_low, maind_high)
            else:
                chance[i, j] = random.randint(rel_low, rel_high)
    return chance


f = 3  # number of features
n = 300  # initial number of beings
per = 5  # lower percentage of population
mutate_per = 1  # chance to mutate to an advanced specie
epochs = 1000  # number of generations
food_lower = 180  # least amount of food
food_higher = 360  # most amount of food
types_of_beings = 50  # max types of beings

if __name__ == "__main__":
    histogramData = list()
    # The different types of species in the system
    qualities = []
    while (len(qualities) != types_of_beings):
        ele = [random.randint(2, 8) for i in range(f)]
        # Each of them have 'f' features and how much a species excels in that feature
        # is given by a number from 1 to 10
        if (ele not in qualities):
            qualities.append(ele)

    # Chance matrix decides how much a feature influences the survival chance of that being
    ones_mat = np.ones((f, 1))
    chance = generate_chance(f, 3, 6, -1, 1)
    qualities_dict = generate_qualdict(qualities, chance, ones_mat)
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

    food_list = [
        random.randint(food_lower, food_higher) for i in range(epochs)
    ]  # resource available for each generation
    barHeights = list()
    for i in range(epochs + 1):  # number of epochs (generations)
        if (not int(i % 100) and i > 0):
            final_popul_dict = dict((i, populist.count(i))
                                    for i in range(1, types_of_beings + 1)
                                    if populist.count(i))
            print("Running epoch_set:", i)
            print(final_popul_dict)
            plotData = sorted(populist)
            for i in range(types_of_beings):
                if final_popul_dict.get(i):
                    barHeights.append(final_popul_dict[i])
                else:
                    barHeights.append(0)
            # histogramData.append(plotData)
            # print(plotData)
            # print("\n\n")
            # Prints the population for every 100 epochs

        # populmatrix is the array of lists with each list containing the features of the species
        # that the being belongs to
        populmatrix = np.array([qualities_dict[i] for i in populist])

        # The produce of the chance and population matrix gives the array of the chance of survival
        result = populmatrix.dot(chance).dot(ones_mat)

        # The results of the probability is normalized to be in between 0 and 1 to use RNG to
        # Decide the survival of that being
        result_norm = np.asarray(
            np.interp(result, (result.min(), result.max()),
                      (0, 1))).reshape(-1)
        # print(result_norm)
        new_populist = [0]
        for j in range(food_list[i]):
            # For each food item on the ith day

            # Food lucky decides whether the each being in the population gets food
            # In that particular epoch
            new_birth = food_lucky(result_norm, populist)

            # The new_populist contains the modified species of the previous population
            new_populist.append(
                mutator(new_birth, qualities_dict, chance, mutate_per,
                        ones_mat))
        populist = new_populist

    # histogramData.append(final_popul_dict.copy())
    # print(plotData)
    print("init_dict")
    print(init_popul_dict)
    print("final_dict")
    print(final_popul_dict)
# %%
    init_keys=[i for i in range(types_of_beings)]
    init_val=[]
    for i in range(types_of_beings):
        if(i in init_popul_dict):
            init_val.append(init_popul_dict[i])
        else:
            init_val.append(0)
    dz=np.array(init_val)
    colors=cm.gnuplot((dz-dz.min())/np.float_(dz.max()-dz.min()))
    plt.bar(init_keys,init_val,color=colors)
    plt.xlabel("Being Types (sorted based on profitable traits)")
    plt.ylabel("Number of Beings")
    #plt.savefig("plot_init.png")
    plt.show()
    final_keys=[i for i in range(types_of_beings)]
    final_val=[]
    for i in range(types_of_beings):
        if(i in final_popul_dict):
            final_val.append(final_popul_dict[i])
        else:
            final_val.append(0)
    dz=np.array(final_val)
    colors=cm.gnuplot((dz-dz.min())/np.float_(dz.max()-dz.min()))
    plt.bar(final_keys,final_val,color=colors)
    plt.xlabel("Being Types (sorted based on profitable traits)")
    plt.ylabel("Number of Beings")
    #plt.savefig("plot_final.png")
    plt.show()
# %%
    fig = pylab.figure()
    ax = Axes3D(fig)
    x = list()
    y = list()
    for day in range(10):
        for species in range(types_of_beings):
            y.append(day)
            x.append(species)
    z = [0 for i in range(10 * types_of_beings)]
    dx = 1
    dy = 1
    dz = np.array(barHeights)
    x = np.array(x)
    y = np.array(y)
    ax.set_xlabel("Species Index")
    ax.set_ylabel("Time")
    ax.set_zlabel("Population")
    values=(dz-dz.min())/np.float_(dz.max()-dz.min())
    colors = cm.gist_heat(values)
    #colors = cm.gnuplot2(values)
    #colors = cm.rainbow(values)
    ax.bar3d(x, y, z, dx, dy, dz, shade=True,color=colors)
    plt.show()


# %%
