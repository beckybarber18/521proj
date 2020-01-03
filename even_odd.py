#!/usr/bin/env python

#-----------------------------------------------------------------------
# even_odd.py
# Author: Rebecca Barber
# 
# takes as input num_trials, max_bidders, num_items
# THIS AUCTION is just like the auction described in the paper, with the
# following modification:
# instead give medium bidders either the even or odd items, 
# uniformly at random (and the other set to the next medium bidder). 
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
def auction_rev(n, m):

	# for each bidder, stores array of length m that stores
	# value for each item
	# bidder_vals will be length n
	bidder_vals = []

	# for each bidder, draw values for each item
	for i in range(n):
		bidder_vals.append(draw_vals(m))

	# who is medium?
	# if sum of values is > mq 
	# (i think this is still the case?)
	q = sqrt(n)
	thresh = m * q
	num_med = 0
	for i in range(len(bidder_vals)):
		val_grand_bundle = sum(bidder_vals[i])
		if val_grand_bundle >= thresh: 
			num_med += 1

	this_rev = 0
    # if there are >= 2 medium bidders, we get revenue m * q
	if num_med >= 2: this_rev = m * q
    # if there is 1 medium bidder, let's say that we give them the
    # even items w.p. 1/2 and odd items w.p. 1/2, so get revenue 
    # m/2 * q
	elif num_med == 1:  this_rev = m/2 * q
    # if there are no medium bidders, we get revenue 0
	else: this_rev = 0
	return this_rev, num_med


def main(argv):

	num_trials = 20
	# num_trials = int(argv[1])
	max_bidders = 30
	# max_bidders = int(argv[2])
	max_items = 10
	min_items = 2
	# max_items = int(argv[3])
	subplot_rows = 3
	subplot_cols = 3

	figure_name = './figures/evenodd' + str(max_bidders) + 'bidders_' + \
			str(max_items) + 'items_' + str(num_trials) + 'trials.png'

	num_bidders = []
	for i in range(2, max_bidders+1):
		num_bidders.append(i)

	item_numbers = []
	for i in range(min_items, max_items+1):
		item_numbers.append(i)

	# store avg revs over n for each number of items
	all_avg_revs_over_n = []

	for num_items in range(min_items, max_items+1):

		print('\nnumber of items:', num_items)

		csv_file = './auction_results/evenodd' + str(max_bidders) + 'bidders_' + \
			str(num_items) + 'items_' + str(num_trials) + 'trials.csv'

		# stores avg rev for n bidder (where n in [2, max_bidders])
		avg_revs_over_n = []
		avg_num_med_over_n = []
		for n in range(2, max_bidders+1):
			print('number of bidders:', n)

			# run num_trials for each # of bidders so we can 
			# take the average
			all_revs = []
			all_num_med = []
			for i in range(num_trials):
				rev, num_med = auction_rev(n, num_items)
				all_revs.append(rev)
				all_num_med.append(num_med)

			avg_rev = mean(all_revs)
			avg_num_med = mean(all_num_med)
			avg_revs_over_n.append(avg_rev)
			avg_num_med_over_n.append(avg_num_med)

		# print and graph avg revs
		for i in range(len(avg_revs_over_n)):
			print('num bidders:', str(i+2), '   avg rev:', avg_revs_over_n[i])

		df = pd.DataFrame(columns=['num bidders', 'avg rev', 'avg num med'])
		for i in range(len(num_bidders)):
			n = num_bidders[i]
			avg_rev = avg_revs_over_n[i]
			avg_num_med = avg_num_med_over_n[i]
			df = df.append({'num bidders': n, 'avg rev': avg_rev, 
				'avg num med': avg_num_med}, ignore_index=True)

		df.to_csv(csv_file)

		# add this data to the large array
		all_avg_revs_over_n.append(avg_revs_over_n)

	# graph avg revs
	fig, axes = plt.subplots(nrows=subplot_rows,ncols=subplot_cols, sharex=True)

	for j in range(len(all_avg_revs_over_n)):

		# calculate benchmark
		benchmark = []
		for i in range(len(num_bidders)):
			benchmark.append(sqrt(num_bidders[i]) * item_numbers[j])
		bench_name = str(j+min_items) + '* sqrt(n)'
		legend = ['simulation', bench_name]
		title = str(j+min_items) + ' items'

		row_num = int(j / subplot_cols)
		col_num = int(j % subplot_cols)

		print(row_num, col_num)

		axes[row_num, col_num].plot(num_bidders,all_avg_revs_over_n[j])
		axes[row_num, col_num].plot(num_bidders,benchmark)
		axes[row_num, col_num].legend(legend, loc='best')
		axes[row_num, col_num].set_title(title) 

		if row_num == subplot_rows - 1:
			axes[row_num, col_num].set(xlabel='num bidders', ylabel='avg rev')
		else:
			axes[row_num, col_num].set(ylabel='avg rev')

	plt.savefig(figure_name)
	plt.show()


if __name__ == '__main__':
	main(argv)



