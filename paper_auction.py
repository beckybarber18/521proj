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

	num_trials = 100
	# num_trials = int(argv[1])
	max_bidders = 80
	# max_bidders = int(argv[2])
	max_items = 7
	# max_items = int(argv[3])
	subplot_rows = 2
	subplot_cols = 3

	num_bidders = []
	for i in range(2, max_bidders+1):
		num_bidders.append(i)

	item_numbers = []
	for i in range(2, max_items+1):
		item_numbers.append(i)

	# store avg revs over n for each number of items
	all_avg_revs_over_n = []

	for num_items in range(2, max_items+1):

		print('\nnumber of items:', num_items)

		csv_file = './auction_results/' + str(max_bidders) + 'bidders_' + \
			str(num_items) + 'items_' + str(num_trials) + 'trials.csv'

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

		df = pd.DataFrame(columns=['num bidders', 'avg rev'])
		for i in range(len(num_bidders)):
			n = num_bidders[i]
			avg_rev = avg_revs_over_n[i]
			df = df.append({'num bidders': n, 'avg rev': avg_rev}, ignore_index=True)

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
		bench_name = str(j+2) + '* sqrt(n)'
		legend = ['simulation', bench_name]
		title = str(j+2) + ' items'

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

	# legend = []
	# for i in range(2, max_items+1):
	# 	legend.append(str(i) + ' items')
	# legend.append('benchmark')

	# fig, ax = plt.subplots()
	# for i in range(len(all_avg_revs_over_n)):
	# 	ax.plot(num_bidders,all_avg_revs_over_n[i])
	# ax.plot(num_bidders, benchmark)
	# plt.legend(legend, loc='lower right')
	# title = '(paper) avg auction revenue over n bidders'
	# plt.xlabel('num bidders') 
	# plt.ylabel('avg rev') 
	# plt.title(title) 
	plt.show()


if __name__ == '__main__':
	main(argv)



