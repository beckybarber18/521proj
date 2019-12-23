#!/usr/bin/env python

#-----------------------------------------------------------------------
# paper_auction.py
# Author: Rebecca Barber
# 
# takes as input num_trials, max_bidders, num_items
#-----------------------------------------------------------------------

import scipy.stats as st
from statistics import *
import matplotlib.pyplot as plt
from sys import argv
import numpy as np
from math import *
import pandas as pd

# private class to define the ER curve
class er_dist(st.rv_continuous):
    def _cdf(self,x):
        return 1-1/x

# draws and returns m values from the ER curve
# i.e. draws all values for single bidder
def draw_vals(m):

	my_cv = er_dist(a = 0, name='er_dist')
	vals = []
	for i in range(m):
		vals.append(my_cv.rvs())
	return vals

# generates revenue for auction given n bidders and 
# m items
def auction_rev(n, m):

	# for each bidder, stores array of length m that stores
	# value for each item
	# bidder_vals will be length n
	bidder_vals = []

	# for each bidder, draw values for each item
	for i in range(n):
		bidder_vals.append(draw_vals(m))

	# who is medium?
	# if you value the grand bundle at least m * q
	q = sqrt(n)
	thresh = m * q
	# medium_flag = []
	num_med = 0
	for i in range(len(bidder_vals)):
		val_grand_bundle = sum(bidder_vals[i])
		if val_grand_bundle >= thresh: 
			# medium_flag.append(True)
			num_med += 1
		# else:
		# 	medium_flag.append(False)

	# we get revenue min(num_med, m) * q
	return min(num_med, m) * q


def main(argv):

	num_trials = 20
	# num_trials = int(argv[1])
	max_bidders = 20
	# max_bidders = int(argv[2])
	num_items = 2
	# num_items = int(argv[3])

	csv_file = './auction_results/' + str(max_bidders) + 'bidders' + str(num_items) + 'items' + str(num_trials) + 'trials.csv'

	# stores avg rev for n bidder (where n in [2, max_bidders])
	avg_revs_over_n = []
	for n in range(2, max_bidders+1):
		print('number of bidders:', n)

		# run num_trials for each # of bidders so we can 
		# take the average
		all_revs = []
		for i in range(num_trials):
			rev = auction_rev(n, num_items)
			all_revs.append(rev)

		avg_rev = mean(all_revs)
		avg_revs_over_n.append(avg_rev)

	# print and graph avg revs
	for i in range(len(avg_revs_over_n)):
		print('num bidders:', str(i+2), '   avg rev:', avg_revs_over_n[i])

	
	num_bidders = []
	for i in range(2, max_bidders+1):
		num_bidders.append(i)

	df = pd.DataFrame(columns=['num bidders', 'avg rev'])
	for i in range(len(num_bidders)):
		n = num_bidders[i]
		avg_rev = avg_revs_over_n[i]
		df = df.append({'num bidders': n, 'avg rev': avg_rev}, ignore_index=True)

	df.to_csv(csv_file)

	# graph avg revs
	fig, ax = plt.subplots()
	ax.plot(num_bidders,avg_revs_over_n)
	title = 'avg auction revenue over n bidders'
	plt.xlabel('num bidders') 
	plt.ylabel('avg rev') 
	plt.title(title) 
	plt.show()


if __name__ == '__main__':
	main(argv)



