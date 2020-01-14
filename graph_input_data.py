#!/usr/bin/env python

#-----------------------------------------------------------------------
# graph_input_data.py
# Author: Rebecca Barber
# 
# just make pretty graph of input data
#-----------------------------------------------------------------------

import scipy.stats as st
from statistics import *
import matplotlib.pyplot as plt
from sys import argv
import numpy as np
from math import *
import pandas as pd
from plotnine import *


def main(argv):

	filename = './auction_results/compiled_bidder_likelihood2to30items_400trials.csv'
	df = pd.read_csv(filename) 
	df = df.rename(columns={"bidders": "Number of Bidders"})

	# x_labels = []
	# for i in range(max_bidders + 1):
	# 	if i % 20 == 0: x_labels.append(i)
	# 	else: x_labels.append('')

	figure_name = './figures/compiled_bidder_likelihood2to30items_400trials.png'

	plt1 = ggplot(aes(x='items', y = 'prob', color = 'Number of Bidders', group = 'Number of Bidders'), data=df) + \
		geom_line() + \
		theme(axis_text_x = element_text(color = 'black'), axis_text_y = element_text(color = 'black')) + \
		labs(x="Number of Items", y="Pr[bidder is medium]") # + \
		# scale_x_discrete(labels = x_labels)

	ggsave(filename=figure_name,
       plot=plt1,
       device='png', dpi = 200)


if __name__ == '__main__':
	main(argv)



