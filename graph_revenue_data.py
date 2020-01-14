#!/usr/bin/env python

#-----------------------------------------------------------------------
# graph_input_data.py
# Author: Rebecca Barber
# 
# just make pretty graph of revenue data
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

	csv_file = './auction_results/compiled_evenodd_80bidders_7items_100trials.csv'
	title = "Even-Odd Revenue"
	df = pd.read_csv(csv_file) 
	df["Legend"] = ""

	print("data loaded")

	nrows = len(df)
	max_bidders = 0
	for i in range(nrows): 
		df.loc[i, "Legend"] = "Simulation"
		num_items =  df.loc[i, "num items"]
		benchmark_val = sqrt(df.loc[i, "num bidders"]) * num_items
		df.loc[i, "num items"] = str(int(num_items)) + " items"
		if df.loc[i, "num bidders"] > max_bidders: max_bidders = df.loc[i, "num bidders"]
		df.loc[len(df)]=[df.loc[i, "num items"], df.loc[i, "num bidders"], benchmark_val, "Benchmark"] 

	x_labels = []
	for i in range(max_bidders + 1):
		if i % 20 == 0: x_labels.append(i)
		else: x_labels.append('')

	print(df.head)

	figure_name = './figures/compiled_evenodd_80bidders_7items_100trials.png'

	plt1 = ggplot(aes(x='num bidders', y = 'avg rev', color = 'Legend', group = 'Legend'), data=df) + \
		geom_line(size = 0.8) + \
	    facet_wrap(['num items']) + \
		theme(axis_text_x = element_text(color = 'black'), axis_text_y = element_text(color = 'black')) + \
		labs(x="Number of Bidders", y="Average Revenue", title = title)

	ggsave(filename=figure_name,
		plot=plt1, device='png', dpi = 300, height = 5, width = 9)


if __name__ == '__main__':
	main(argv)

