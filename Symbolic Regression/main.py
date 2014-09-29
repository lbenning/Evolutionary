#! /usr/bin/python

from gp import simulate
from gp import randomSearch
from threading import Thread
from plot import graph
import sys

'''
Main script for execution of genetic program for 
symbolic regression.

Written by Luke Benning
Last Edited : 9/27/2014
'''

global res
global kingRes
global randRes

# Base GP simulation
# Run single genetic simulation - tree height 5
def runGenetic(data, eva, count):
	res.append(simulate(data,eva,count,False))

# Run genetic - king of the hill - tree height 5
def runGeneticKing(data,eva,count):
	kingRes.append(simulate(data,eva,count,True))

# Run single random simulation
def runRandom(data, eva, count):
	randRes.append(randomSearch(data,eva,count))

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

# Finds best equation
def findBestEquation(r,s):
	bestScore = -1.0
	bestEqn = "None"
	for x in r:
		if (x[0][len(x[0])-1] > bestScore):
			bestScore = x[0][len(x[0])-1]
			bestEqn = x[1]
	for x in s:
		if (x[0][len(x[0])-1] > bestScore):
			bestScore = x[0][len(x[0])-1]
			bestEqn = x[1]
	return bestEqn

# Initialize full genetic program simulation
def main(filename, iterations, eva, count):

	global res
	res = []
	global randRes
	randRes = []
	global kingRes
	kingRes = []

	data = getData(filename)

	intervals = []
	intervals.append(1)
	for x in range(1,count+1):
		intervals.append(x*(eva/count))

	for x in range(iterations):
		t = Thread(target=runGenetic,args=(data,eva,intervals))
		t.start()
		t.join()
		s = Thread(target=runRandom,args=(data,eva,intervals))
		s.start()
		s.join()
		k = Thread(target=runGeneticKing,args=(data,eva,intervals))
		k.start()
		k.join()

	print "Simulation Complete"
	print "Best Equation Found: "
	print findBestEquation(res,kingRes)
	
	graph(selectFirst(res),selectFirst(randRes),selectFirst(kingRes),intervals)

'''
arg1 : Filename to read in list of 2d points
arg2 : Number of iterations n > 0
arg3 : Number of evaluations m > 0
arg4 : Number of interval points to plot i > 0 (in addition to 1)
'''
if __name__ == '__main__':
    main(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]))