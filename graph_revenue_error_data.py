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
	title = "Even-Odd Simulation Error"
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
		df.loc[i, "error"] = abs(benchmark_val - df.loc[i, "avg rev"])
		if df.loc[i, "num bidders"] > max_bidders: max_bidders = df.loc[i, "num bidders"]

	x_labels = []
	for i in range(max_bidders + 1):
		if i % 20 == 0: x_labels.append(i)
		else: x_labels.append('')

	print(df.head)

	figure_name = './figures/evenodd_differences.png'
	df = df.rename(columns={"num items": "Number of Items"})

	plt1 = ggplot(aes(x='num bidders', y = 'error', color = 'Number of Items', group = 'Number of Items'), data=df) + \
		geom_point(size = 1.5) + \
		theme(axis_text_x = element_text(color = 'black'), axis_text_y = element_text(color = 'black')) + \
		labs(x="Number of Bidders", y="Error (| realized revenue - benchmark |)", title = title) # + \
		# scale_x_discrete(labels = x_labels)

	ggsave(filename=figure_name,
       plot=plt1,
       device='png', dpi = 200, width = 9, height = 5)


if __name__ == '__main__':
	main(argv)

