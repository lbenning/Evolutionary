#! /usr/bin/python

from gp import simulate
from gp import randomSearch
import multiprocessing as mp
from plot import graph
import sys

'''
Main script for execution of genetic program for 
symbolic regression.

Written by Luke Benning
Last Edited : 1/16/2015
'''

# Retrieve 2d point data from file
def getData(fileName):
	points = []
	f = open(fileName,'r')
	for line in f:
  		s = line.split(" ")
  		f = []
  		for y in s:
  			if (not y == ''):
  				f.append(y)
  		x = (float(f[0]), float(f[1]))
  		points.append(x)
  	return points

# Retrieve first elements in tuples
def selectFirst(k):
	trimmed = []
	for t in k:
		trimmed.append(t[0])
	return trimmed

# Finds best equation among the simulation results
def findBestEquation(tradGeneticRes,randomRes):
	bestScore = -1.0
	bestEqn = "None"
	for x in tradGeneticRes:
		if (x[0][len(x[0])-1] > bestScore):
			bestScore = x[0][len(x[0])-1]
			bestEqn = x[1]
	for x in randomRes:
		if (x[0][len(x[0])-1] > bestScore):
			bestScore = x[0][len(x[0])-1]
			bestEqn = x[1]
	return bestEqn

# Initialize full genetic program simulation
def main(filename, iterations, eva, count, processCt):

	print "Retrieving dataset..."

	data = getData(filename)

	intervals = []
	intervals.append(1)
	for x in range(1,count+1):
		intervals.append(x*(eva/count))

	processPool = mp.Pool(processes=processCt)

	print "Beginning simulations..."

	geneticJobs = [processPool.apply_async(simulate,
	 args=(data,eva,intervals)) for x in range (iterations)]

	randomJobs = [processPool.apply_async(randomSearch,
	 args=(data,eva,intervals)) for x in range (iterations)]

	res = [g.get() for g in geneticJobs]
	randRes = [r.get() for r in randomJobs]

	print "Simulation Complete"
	print "Best Equation Found: "
	print findBestEquation(res,randRes)
	
	graph(selectFirst(res),selectFirst(randRes),intervals)

'''
arg1 : Filename to read in list of 2d points
arg2 : Number of iterations n > 0
arg3 : Number of evaluations m > 0
arg4 : Number of interval points to plot i > 0 (in addition to 1)
arg5 : Maximum number of processes for multiprocessing pool
'''
if __name__ == '__main__':
    main(sys.argv[1],
    	int(sys.argv[2]),
    	int(sys.argv[3]),
    	int(sys.argv[4]),
    	int(sys.argv[5]))