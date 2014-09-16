import math
import numpy as np

# Distance between 2 2d points
def distance(pta, ptb):
	return math.sqrt((ptb[0]-pta[0])**2 + (ptb[1]-pta[1])**2)

# Fitness function for minimizing distance
def fitnessShort(strat,chart):
	return 1.0 / fitnessLong(strat,chart)

# Fitness function for maximizing distance
def fitnessLong(s,c):
  d = 0.0
  for x in range(len(s)-1):
    d += distance(c[s[x]-1],c[s[x+1]-1])
  d += distance(c[s[0]-1],c[s[len(s)-1]-1])
  return d

# Swap 2 numerical values in a list
def swap(c,x,y):
	if (not x == y):
		c[x] = c[x]+c[y]
		c[y] = c[x]-c[y]
		c[x] = c[x]-c[y]

def getData(fileName):
	points = []
	f = open(fileName,'r')
	for line in f:
  		s = line.split(" ")
  		x = (float(s[0]), float(s[1]))
  		points.append(x)
  	return points

def errorBars(data,inter):
	devs = []
	for x in range(len(data[0])):
		n = np.arange(0,len(data))
		for y in range(len(data)):
			n[y] = data[y][x]
		devs.append(np.std(n)/math.sqrt(inter[x]))
	return devs