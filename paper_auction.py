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
from plotnine import *

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
	this_rev = min(num_med, m) * q
	return this_rev, num_med


def main(argv):

	num_trials = 100
	# num_trials = int(argv[1])
	max_bidders = 100
	# max_bidders = int(argv[2])
	max_items = 7
	min_items = 2
	# max_items = int(argv[3])
	# subplot_rows = 2
	# subplot_cols = 2

	num_bidders = []
	for i in range(2, max_bidders+1):
		num_bidders.append(i)

	item_numbers = []
	for i in range(min_items, max_items+1):
		item_numbers.append(i)

	# store avg revs over n for each number of items
	all_avg_revs_over_n = []

	figure_name = './figures/' + str(max_bidders) + 'bidders_' + \
			str(max_items) + 'items_' + str(num_trials) + 'trials.png'

	for num_items in range(min_items, max_items+1):

		print('\nnumber of items:', num_items)

		csv_file = './auction_results/' + str(max_bidders) + 'bidders_' + \
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

	# make dataframe for plotting
	rev_df = pd.DataFrame(columns=['num items', 'num bidders', 'avg rev', 'Legend'])
	for i in range(len(all_avg_revs_over_n)):
		these_revs = all_avg_revs_over_n[i]
		m = i + min_items
		for j in range(len(these_revs)):
			n = j + 2
			rev = these_revs[j]
			benchmark = m * sqrt(n)
			item_str = str(int(m)) + ' items'
			rev_df = rev_df.append({'num items': item_str, 'num bidders': n, 'avg rev': rev, 'Legend': 'Simulation'}, 
				ignore_index=True)
			rev_df = rev_df.append({'num items': item_str, 'num bidders': n, 'avg rev': benchmark, 'Legend': 'Benchmark'}, 
				ignore_index=True)

	x_labels = []
	for i in range(max_bidders + 1):
		if i % 20 == 0: x_labels.append(i)
		else: x_labels.append('')

	plt1 = ggplot(aes(x='num bidders', y = 'avg rev', color = 'Legend', group = 'Legend'), data=rev_df) + \
		geom_line() +\
	    facet_wrap(['num items']) + \
		theme(axis_text_x = element_text(color = 'black'), axis_text_y = element_text(color = 'black')) + \
		labs(x="Number of Bidders", y="Average Revenue", title = "Many-Medium Revenue") + \
		scale_x_discrete(labels = x_labels)

	ggsave(filename=figure_name,
       plot=plt1,
       device='png', dpi = 200)


	# fig, axes = plt.subplots(nrows=subplot_rows,ncols=subplot_cols, sharex=True)
	# plt.figure(dpi=100)
	# plt.style.use('ggplot')

	# for j in range(len(all_avg_revs_over_n)):

	# 	# calculate benchmark
	# 	benchmark = []
	# 	for i in range(len(num_bidders)):
	# 		benchmark.append(sqrt(num_bidders[i]) * item_numbers[j])
	# 	bench_name = str(j+min_items) + '* sqrt(n)'
	# 	legend = ['simulation', bench_name]
	# 	title = str(j+min_items) + ' Items'

	# 	row_num = int(j / subplot_cols)
	# 	col_num = int(j % subplot_cols)

	# 	print(row_num, col_num)

	# 	axes[row_num, col_num].plot(num_bidders,all_avg_revs_over_n[j])
	# 	axes[row_num, col_num].plot(num_bidders,benchmark)
	# 	axes[row_num, col_num].legend(legend, loc='best')
	# 	axes[row_num, col_num].set_title(title) 

	# 	if row_num == subplot_rows - 1:
	# 		axes[row_num, col_num].set(xlabel='Number of Bidders', ylabel='Average Revenue')
	# 	else:
	# 		axes[row_num, col_num].set(ylabel='Average Revenue')

	# plt.savefig(figure_name) 
	# plt.show()


if __name__ == '__main__':
	main(argv)



