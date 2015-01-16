#! /usr/bin/python

from genetic import genetic
from parametric import stochClimb
from parametric import randSearch
from tools import getData
from plot import graph
import sys
import multiprocessing as mp

'''
Main file for launching TSP Learner.
Script requires 5 arguments:

arg1 - File name containing list of 2d points
arg2 - Number of simulations per algorithm
arg3 - Evaluations per simulations
arg4 - Number of times to record path length per simulation (exxcluding initial evaluation)
'''

# Simulate genetic algorithms and parametric optimizers and display
# 	graph depicting algorithm performance of fitness vs. evaluations
# arg name : Filepath to dataset
# arg iterations : Number of simulation for each algorithm
# arg eva : Number of fitness function evaluations per simulation
# arg count : Number of times to record fitness, spread uniformly over
# 	number of fitness function evaluations
# arg processCt : Number of processes for the multiprocessing pool
def main(name,iterations,eva,count,processCt):

	data = getData(name)	
	intervals = []
	intervals.append(1)
	for x in range(1,count+1):
		intervals.append(x*(eva/count))
	evaluations = eva

	travWorkers = mp.Pool(processes=processCt)
	
	genPmxJobs = [travWorkers.apply_async(genetic,
		args=(data,evaluations,intervals,False)) for x in range(iterations)]

	genHalfJobs = [travWorkers.apply_async(genetic,
		args=(data,evaluations,intervals,True)) for x in range(iterations)]

	stochJobs = [travWorkers.apply_async(stochClimb,
		args=(data,evaluations,intervals)) for x in range(iterations)]

	randJobs= [travWorkers.apply_async(randSearch,
		args=(data,evaluations,intervals)) for x in range(iterations)]

	# Close the pool and wait until all processes are finished
	travWorkers.close()
	travWorkers.join()

	# Retrieve process outputs
	genPmx = [t.get() for t in genPmxJobs]
	genHalf = [t.get() for t in genHalfJobs]
	stoch = [t.get() for t in stochJobs]
	rand = [t.get() for t in randJobs]

	# Display graph of simulation results
	graph(genPmx,genHalf,stoch,rand,intervals)

if __name__ == '__main__':
    main(sys.argv[1],
    	int(sys.argv[2]),
    	int(sys.argv[3]),
    	int(sys.argv[4]),
    	int(sys.argv[5]))