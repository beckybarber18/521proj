#https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_continuous.html 

import scipy.stats as st
from statistics import *
import matplotlib.pyplot as plt

class er_dist(st.rv_continuous):
    def _cdf(self,x):
        return 1-1/x

my_cv = er_dist(a = 0, name='er_dist')
samples = []
num_samples = 5000
for i in range(num_samples):
	samples.append(my_cv.rvs())
	if i % 1000 == 0: print('i:', i)

print('mean:', mean(samples))
num_bins = 1000
plt.hist(samples, num_bins)
plt.xlim(0,150)
plt.show()
