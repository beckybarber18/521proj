#!/usr/bin/env python

#-----------------------------------------------------------------------
# bidder_likelihood_over_numitems.py
# Author: Rebecca Barber
# 
# graphs the probability that a bidder is medium over the number of
# items in the auction
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

	my_cv = er_dist(a = 1, name='er_dist')
	vals = []
	for i in range(m):
		vals.append(my_cv.rvs())
	return vals

# generates revenue for auction given n bidders and 
# m items
def compute_probability(n, m):

	# for each bidder, stores array of length m that stores
	# value for each item
	# bidder_vals will be length n
	bidder_vals = []

	# for each bidder, draw values for each item
	for i in range(n):
		bidder_vals.append(draw_vals(m))

	# who is medium?
	# if sum of values is > mq 
	q = sqrt(n)
	thresh = m * q
	num_med = 0
	for i in range(len(bidder_vals)):
		val_grand_bundle = sum(bidder_vals[i])
		if val_grand_bundle >= thresh: 
			num_med += 1

	# prob that someone is medium is just the num_med / total # bidders
	return num_med / n

def main(argv):

	num_trials = 200
	num_bidders = [2, 5, 10, 25]
	max_items = 30
	min_items = 2

	figure_name = './figures/bidder_likelihood' + str(min_items) + 'to' + str(max_items) \
		+ 'items_' + str(num_trials) + 'trials.png' 

	num_items = []
	for i in range(min_items, max_items+1):
		num_items.append(i)

	# store avg probabilities over n for each number of items
	all_avg_probabilities = []

	# for each number of bidders
	for n in num_bidders:
		print('\nnumber of bidders:', n)
		csv_file = './auction_results/bidder_likelihood' + str(min_items) + 'to' + str(max_items) \
				+ 'items_' + str(n) + 'bidders_' + str(num_trials) + 'trials.csv'

		avg_probabilities = []
		for m in num_items:
			print('number of items:', m)

			# run num_trials for each # of items so we can take the avg prob
			probs_for_m_items = []
			for i in range(num_trials):
				prob = compute_probability(n, m)
				probs_for_m_items.append(prob)

			avg_prob_for_m_items = mean(probs_for_m_items)
			avg_probabilities.append(avg_prob_for_m_items)

		# export data to csv files
		df = pd.DataFrame(columns=['num items', 'avg probability'])
		for i in range(len(num_items)):
			m = num_items[i]
			avg_prob = avg_probabilities[i]
			df = df.append({'num items': m, 'avg probability': avg_prob},  ignore_index=True)
			df.to_csv(csv_file)

		# add this data to the large array
		all_avg_probabilities.append(avg_probabilities)

	# graph avg probabilities
	legend = []
	for n in num_bidders:
		legend.append(str(n) + ' bidders')

	plt.figure(dpi=100)
	plt.style.use('ggplot')
	for i in range(len(all_avg_probabilities)):
		plt.plot(num_items, all_avg_probabilities[i])
	plt.legend(legend, loc='best')
	plt.xlabel('Number of Items', color = 'black') 
	plt.ylabel('Pr[bidder is medium]', color = 'black')
	ax = plt.gca()
	ax.tick_params(axis = 'both', which = 'major', labelcolor = 'black')
	ax.tick_params(axis = 'both', which = 'minor',labelcolor = 'black')
	plt.savefig(figure_name) 
	plt.show()


if __name__ == '__main__':
	main(argv)
