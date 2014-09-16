import math
import random
import numpy as np
from tools import *
import sys

'''
Collection of 4 different genetic algorithms to solve TSP - 
Each using either PMX or Half recombination and ranking or 
roulette selection, yielding a total of 4 combinations
'''

# Initialize the population, a collection of paths
def initPopulation(n,m):
	indiv = []
	for a in range(n):
		strat = []
		values = []
		for x in range(1,m+1):
			values.append(x)
		while (len(values) > 0):
			r = random.randint(0,len(values)-1)
			strat.append(values.pop(r))
		indiv.append(strat)
	return indiv

# PMX recombination
def pmxRecomb(x,y,m):
	child = []
	for i in range(len(x)):
		child.append(0)
	p1 = random.randint(0,len(x)/2)
	p2 = random.randint(len(x)/2+1,len(x)-2)
	d = {}
	seen = set()
	for i in range(p1,p2+1):
		d[y[i]] = x[i]
		child[i] = y[i]
		seen.add(y[i])
	for i in range(0,p1):
		j = x[i]
		while (j in seen):
			j = d[j]
		seen.add(j)
		child[i] = j
	for i in range(p2+1,len(x)):
		j = x[i]
		while (j in seen):
			j = d[j]
		seen.add(j)
		child[i] = j
	if (int(random.randint(1,int(1/m))) == 1):
		mutate(child)
	return child

# Half individual recombination
def halfRecomb(x,y,m):
	child = []
	seen = set()
	for i in range(len(x)/2):
		child.append(x[i])
		seen.add(x[i])
	for g in range(len(y)):
		if (not y[g] in seen):
			child.append(y[g])
			if (len(child) >= len(y)):
				break
	if (int(random.randint(1,int(1/m))) == 1):
		mutate(child)
	return child

# Single swap and sequence mutations
def mutate(c):
	if (int(random.randint(1,2)) == 2):
		randX = random.randint(0,len(c)/2-1)
		randY = random.randint(len(c)/2+1,len(c)-1)
		while (randX < randY):
			swap(c,randX,randY)
			randX += 1
			randY -= 1
	else:
		randX = random.randint(0,len(c)-1)
		randY = randX
		while(randX == randY):
			randY = random.randint(0,len(c)-1)
		swap(c,randX,randY)

# Roulette selector
def roulette(scores, value):
	k = value
	x = 0
	while (k >= 0 and x < len(scores)):
		k -= scores[x]
		x += 1
	return scores[x-1][0]

# Mutation degrades over time over a discrete set
def degrade(val):
	if (val >= 5000000):
		return 0.01
	elif (val >= 2500000):
		return 0.02
	elif (val >= 1000000):
		return 0.03
	elif (val >= 600000):
		return 0.20
	elif (val >= 300000):
		return 0.30
	elif (val >= 30000):
		return 0.40
	return 0.50

# Main simulation function
def genetic(points, bound, inter, recFlag, selFlag):
	# Global evaluation counter
	val = 0
	# Mutation rate - will be degraded
	mRate = 0.40
	# Constants
	POP_SIZE = 60
	RECOMB_RATE = 0.4
	# Population & Parent size
	population = initPopulation(POP_SIZE, len(points))
	parentCount = int(POP_SIZE*RECOMB_RATE)
	#  Simulation
	best = float(-1.0)
	data = []
	while (True):
		# Fitness Measurements
		fitnessScores = np.zeros((POP_SIZE,1))
		scoreMap = {}
		for x in range(len(population)):
			fitnessScores[x][0] = fitnessShort(population[x], points)
			if (fitnessScores[x][0] > best):
				topPath = population[x]
				best = fitnessScores[x][0]
			scoreMap[fitnessScores[x][0]] = x
			val += 1
			if (val in inter):
				data.append(1.0/best)
			if (val >= bound):
				return data
			mRate = degrade(val)
		fitnessScores = np.flipud(np.sort(fitnessScores,axis=0))
		par = np.zeros((parentCount,1),dtype=np.int)

		# Selection
		if (selFlag):	
			for x in range(parentCount):
				par[x][0] = scoreMap.get(fitnessScores[x][0])
		else:
			total = np.sum(fitnessScores)
			for x in range(parentCount):
				slot = random.uniform(0,total)
				par[x][0] = scoreMap.get(roulette(fitnessScores,slot))

		# Variation
		children = []
		t = 0
		while(t < parentCount):
			if (recFlag):
				children.append(halfRecomb(population[par[t][0]],population[par[t+1][0]], mRate))
				children.append(halfRecomb(population[par[t+1][0]],population[par[t][0]], mRate))
			else:
				children.append(pmxRecomb(population[par[t][0]],population[par[t+1][0]], mRate))
				children.append(pmxRecomb(population[par[t+1][0]],population[par[t][0]], mRate))
			t+=2
		for x in range(len(population)-parentCount,len(population)):
			population[scoreMap.get(fitnessScores[x][0])] = children.pop()
