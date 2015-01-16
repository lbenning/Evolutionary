import matplotlib.pyplot as plt
import math
import numpy as np

# Plots the simulation results of the algorithms
def graph(genProg,randSearch,intervals):

	genColl = collapse(genProg)
	randColl = collapse(randSearch)

	genBars = errorBars(genProg,intervals)
	randBars = errorBars(randSearch,intervals)

	plt.plot(intervals,genColl,"red",
		intervals,randColl,"blue")

	plt.ylabel('Fitness (Base e)')
	plt.xlabel('Evaluations')
	plt.title('GP Symbolic Regression')

	for x in range(len(intervals)):
		plt.errorbar(intervals[x], genColl[x], yerr=genBars[x], linestyle="None", marker="None", color="orange")
		plt.errorbar(intervals[x], randColl[x], yerr=randBars[x], linestyle="None", marker="None", color="black")
		
	plt.show()

# Retrieve best results over multiple simulations
# of each algorithm
def collapse(data):
	t = []
	for x in range(len(data[0])):
		best = -1.0
		for y in range(len(data)):
			if (data[y][x] > best):
				best = data[y][x]
		t.append(best)
	return t

# Computes error bars for multiple simulations on
# each algorithm - represented as standard deviation
# over the square root of the number of iterations
def errorBars(data,inter):
	devs = []
	for x in range(len(data[0])):
		n = np.arange(0,len(data))
		for y in range(len(data)):
			n[y] = data[y][x]
		devs.append(np.std(n)/math.sqrt(inter[x]))
	return devs