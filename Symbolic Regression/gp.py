'''
Core Class for Genetic Program

Simulation mechanism that runs the genetic program at a high level,
and delegates the specific mechanics elsewhere.

'''

import numpy as np
import sympy
from trees import *

# Random Search over state space of formulas
def randomSearch(p,eva,interv):
	fitness = randomTreeScore(p)
	ctr = 0
	points = []
	while (fitness == -1.0 and ctr < eva):
		fitness = randomTreeScore(p)
		ctr += 1
		if (ctr in interv):
			points.append(fitness)
	while (ctr < eva):
		j = randomTreeScore(p)
		if (j > fitness):
			fitness = j
		ctr += 1
		if (ctr in interv):
			points.append(fitness)
	return (points,"x+x")

# Degrade the mutation rate over time - increases
# initial convergenge rate while avoiding the
# destruction of good genes that are evolved
def degradeMutation(eva):
	if (eva <= 100000):
		return 0.55
	elif (eva <= 200000):
		return 0.30
	elif (eva <= 500000):
		return 0.15
	elif (eva <= 800000):
		return 0.08
	elif (eva <= 1500000):
		return 0.04
	else:
		return 0.02

# Genetic programming simulation
def simulate(data, eva, interv, king):

	# Constants
	# Recombination rate
	RECOMBRATE = 0.35
	# Population size
	POPSIZE = 60

	# Number of time fitness function evaluated
	ctr = 0;
	# Mutation rate - will be degraded
	mRate = 0.40
	# Initial Population - 60 trees
	pop = generateForest(POPSIZE)
	# Best tree score
	maxScore = 0.0
	# Best tree equation
	maxEquation = None
	# Scores
	scores = []

	while(True):
		fitnessScores = np.zeros(len(pop))
		scoreMap = {}
		for t in range(len(pop)):
			fitnessScores[t] = treeFitness(pop[t], data)
			scoreMap[fitnessScores[t]] = t
			# Check if new best
			if (fitnessScores[t] > maxScore):
				maxScore = fitnessScores[t]
				maxEquation = pop[t]
			ctr += 1
			# Measure best soln. found so far periodically
			if (ctr in interv):
				scores.append(maxScore)
				if (ctr >= eva):
					s = sympy.simplify(treeString(maxEquation))
					return (scores,s)

		mRate = degradeMutation(ctr)

		# Sort scores in descending order
		fitnessScores = np.flipud(np.sort(fitnessScores,axis=0))

		# Perform recombination & mutation - Every parent pair
		# produces two children
		children = []
		for x in range(int(POPSIZE*RECOMBRATE/2)):
			p1 = pop[scoreMap[fitnessScores[x]]]
			p2 = pop[scoreMap[fitnessScores[x+1]]]
			outcomes = recombTrees(p1,p2,mRate)
			children.append(outcomes[0])
			children.append(outcomes[1])

		# Record children length
		cLength = len(children)

		# Replace the poorest performing individuals
		for x in range(len(pop)-len(children),len(pop)):
			pop[scoreMap[fitnessScores[x]]] = children.pop()

		if (king):
			# King of the hill - Let the top performing individual
			# replace a small portion of lower scoring individuals with
			# it's genetic data, if it beats out all of them by at least
			# a factor of 2.
			if (fitnessScores[0]/fitnessScores[len(pop)-cLength] >= 2.0):
				for x in range(len(pop)-cLength-3,len(pop)-cLength):
					pop[scoreMap[fitnessScores[x]]] = pop[scoreMap[fitnessScores[0]]]
		