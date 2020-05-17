# %%
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import math

mu = 1
variance = 15/45
sigma = math.sqrt(variance)
x = np.linspace(0, 1, 100)
plt.plot(x, stats.norm.pdf(x, mu, sigma))
plt.show()

# %%
