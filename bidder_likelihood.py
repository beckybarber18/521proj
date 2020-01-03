#https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_continuous.html 

import scipy.stats as st
from statistics import *
import matplotlib.pyplot as plt
import numpy as np
import math

class er_dist(st.rv_continuous):
    def _cdf(self,x):
        return 1-1/x

my_cv = er_dist(a = 1, b = 20000, name='er_dist')


# --- Calculate likelihood a single bidder's total value is over mq --- #

m = 2  # number of items
q_vals = 200
num_greater = np.zeros(q_vals + 1)  # num_greater[i] = count(total_val > m * i)
num_samples = 10000

for i in range(num_samples):
	bidder_vals = my_cv.rvs(size=m)
	highest_q = math.floor(np.sum(bidder_vals) / m)  # the highest q-value that would make the bidder be medium
	if highest_q > q_vals:
		highest_q = q_vals
	num_greater[0:(highest_q + 1)] += 1
	if i % 2000 == 0:
		print(i)

proportion_greater = num_greater / num_samples

plt.plot(proportion_greater)
plt.show()

# plot 2/(2q-1) + ((q - 0.5) * ln(2q-1) - q)/(q^2(2q-1))