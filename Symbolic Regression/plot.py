import matplotlib.pyplot as plt
import math
import numpy as np

# Plots the simulation results of the algorithms
def graph(genProg,randSearch,genKing,intervals):

	logScale(genProg)
	logScale(randSearch)
	logScale(genKing)

	genColl = collapse(genProg)
	randColl = collapse(randSearch)
	kingColl = collapse(genKing)

	genBars = errorBars(genProg,intervals)
	randBars = errorBars(randSearch,intervals)
	genKingBars = errorBars(genKing,intervals)

	plt.plot(intervals,genColl,"red",
		intervals,randColl,"blue",
		intervals,kingColl,"green")

	plt.ylabel('Fitness (Base e)')
	plt.xlabel('Evaluations')
	plt.title('GP Symbolic Regression : Division - Noise')

	for x in range(len(intervals)):
		plt.errorbar(intervals[x], genColl[x], yerr=genBars[x], linestyle="None", marker="None", color="red")
		plt.errorbar(intervals[x], randColl[x], yerr=randBars[x], linestyle="None", marker="None", color="blue")
		plt.errorbar(intervals[x], kingColl[x], yerr=genKingBars[x], linestyle="None", marker="None", color="green")

	plt.show()

# Logarithmically scales values
def logScale(data):
	for x in range(len(data)):
		for y in range(len(data[x])):
			data[x][y] = math.log(data[x][y])

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