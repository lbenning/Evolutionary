#! /usr/bin/python
# Iterated Prisoner's Dilemma Simulation
# Author : Luke Benning
# Last Edited : 5/20/2014

import random

# Initializes x agents with y length action list
# 0 - Cooperate, 1- Defect, where
# defect means admitting to the crime and consequently 
# cooperating means not admitting to the crime.
# Strategy can look 4 moves back.
def initAgents(x):
	indiv = []
	for k in range(x):
		j = []
		for i in range(271):
			j.append(random.randint(0,1))
		indiv.append(j)
	return indiv

#Locate agent probabilistically
def findAgent(pts,sumx):
	partial = 0
	for r in range(0,len(pts)):
		if ((partial + pts[r]) >= sumx):
			return r
		else:
			partial += pts[r]

# Combine action sequences of 2 individuals to generate 2 children.
def recombinator(a1,a2,bound):
	child1 = []
	child2 = []
	for x in range(0,bound):
		child1.append(a1[x])
		child2.append(a2[x])
	for y in range(bound,len(a1)):
		child1.append(a2[y])
		child2.append(a1[y])
	f = []
	f.append(child1)
	f.append(child2)
	return f

# Mutate fraction of action sequence
def mutate(c):
	change = random.randint(1,5)
	region = random.randint(change,len(c[0]))
	for k in range(change):
		index = region - (k+1)
		c[0][index] = random.randint(0,1)
		c[1][index] = random.randint(0,1)
	return c


# Evolutionary constants
ips = 10 # Init. Pop. Size
mutation = 0.005 # Probability of mutation
generations = 100 # Generations to evolve population
recombination = 0.8 # Recombination Fraction

# Payoffs
c_d = 0 # Cooperate & Defect
c_c = 3 # Cooperate & Cooperate
d_d = 1 # Defect & Defect
d_c = 5 # Defect & Cooperate

# Create <ips> initial agents
agents = initAgents(ips)

for q in range(generations):

	# Agents cannot know number of games per round, must
	# be randomly determined on each iteration.
	games = random.randint(5,100)
	points = []

	# Init. Agent Point Scores
	for l in range(len(agents)):
		points.append(0)

	# We do not allow an agent to play itself
	for s in range(len(agents)-1):
		for r in range(s+1,len(agents)):
			# On agent pair, play <games>
			s_history = []
			r_history = []
			for k in range(games):
				ag1 = -1
				ag2 = -1
				# First round - no observable history
				if (k == 0):
					ag1 = agents[s][0]
					ag2 = agents[r][0]
				# Second round - 1 observable history
				elif (k == 1):
					a1_ind = 2 - r_history[0]
					ag1 = agents[s][a1_ind]
					a2_ind = 2 - s_history[0]
					ag2 = agents[r][a2_ind]
				# Third round - 2 observable history
				elif (k == 2):
					a1_ind = 6 - 2*r_history[0] - r_history[1]
					ag1 = agents[s][a1_ind]
					a2_ind = 6 - 2*s_history[0] - s_history[1]
					ag2 = agents[r][a2_ind]
				# Fourth round - 3 observable history
				elif (k == 3):
					a1_ind = 14 - 4*r_history[0] - 2*r_history[1] - r_history[2]
					ag1 = agents[s][a1_ind]
					a2_ind = 14 - 4*s_history[0] - 2*s_history[1] - s_history[2]
					ag2 = agents[r][a2_ind]
				# nth round, n > 4 - Observe past 4 results
				else:
					index = (270 - s_history[len(s_history)-4] - 2*s_history[len(s_history)-3] - \
					4*s_history[len(s_history)-2] - 8*s_history[len(s_history)-1] - \
					16*r_history[len(r_history)-4] - 32*r_history[len(r_history)-3] - \
					 64*r_history[len(r_history)-2]- 128*r_history[len(r_history)-1])
					ag1 = agents[s][index]
					ag2 = agents[r][index]

				if (ag1 == 1 and ag2 == 0):
					points[s] += d_c
					points[r] += c_d
				elif (ag1 == 1 and ag2 == 1):
					points[s] += d_d
					points[r] += d_d
				elif (ag1 == 0 and ag2 == 1):
					points[s] += c_d
					points[r] += d_c
				elif (ag1 == 0 and ag2 == 0):
					points[s] += c_c
					points[r] += c_c

				s_history.append(ag1)
				r_history.append(ag2)

	# Produce offspring
	point_sum = 0
	offspring = []
	for h in range(len(points)):
		point_sum += points[h]
	for i in range(int((float(ips)*recombination)/2.0)):
		parent1 = findAgent(points,random.randint(0,point_sum))
		parent2 = findAgent(points,random.randint(0,point_sum))
		# Enforce parents to be unique - No asexual reproduction
		while (parent2 == parent1):
			parent2 = findAgent(points,random.randint(0,point_sum))
		# Produce 2 children from 2 parents
		children = recombinator(agents[parent1],agents[parent2],
			random.randint(5,265))
		# Apply mutations with prob. 1/mutation
		n = random.randint(1,int(float(1)/mutation))
		if (n == 1):
			children = mutate(children)
		# Add 2 children to offspring
		offspring.append(children[0])
		offspring.append(children[1])

	# Remove the same amount of unfit individuals as offspring
	for r in range(len(offspring)):
		x = random.randint(0,len(points)-1)
		del agents[x]
		del points[x]

	for n in range(len(offspring)):
		agents.append(offspring[0])


# Print results		
for i in range(len(agents)):
	print agents[i]
