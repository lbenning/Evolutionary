import math
import random
import numpy
from tools import *

'''
Parametric Optimizers to search for optimal TSP solution. 
Method 1: Stochastic Hill Climbing search
Method 2: Random Search - Used as benchmark
'''

# Initialize the population, a collection of paths
def createPath(m):
  n = numpy.arange(1,m+1)
  numpy.random.shuffle(n)
  return n

# Perform a stochastic hill climbing search
def stochClimb(points,bound,inter):
  p = len(points)
  # ctr for fitness func. eval.
  ctr = 0
  # data taken at each i in inter
  data = []
  # best seen so far
  maxfit = 0.0
  while (ctr < bound):
    # Path
    v = createPath(p)
    f = fitnessShort(v,points)
    if (f > maxfit):
      maxfit = f
    ctr += 1
    if (ctr in inter):
      data.append(1.0/maxfit)
      if (ctr >= bound):
        return data
    # Create swap indices
    o = numpy.arange(v.size)
    i = numpy.arange(v.size)
    while (ctr < bound):
      climbed = False
      numpy.random.shuffle(o)
      numpy.random.shuffle(i)
      for x in range(o.size):
        for y in range(i.size):
          swap(v,o[x],i[y])
          shot = fitnessShort(v,points)
          ctr += 1
          if (shot <= f):
              swap(v,o[x],i[y])
          else:
            f = shot
            climbed = True
          if (ctr in inter):
              if (shot > maxfit):
                maxfit = shot
              data.append(1.0/maxfit)
          if (ctr >= bound):
            return data
      # If no improvement made, local optimum reached
      # Return solution, otherwise keep trying to climb
      if (not climbed):
        break
      else:
        if (f > maxfit):
          maxfit = f

# Perform a random search, used primarily for benchmarking
def randSearch(points,bound,inter):
  p = len(points)
  scores = []
  best = 0.0
  for x in range(1,bound+1):
    z = createPath(p)
    s = fitnessShort(z,points)
    if (s > best):
      best = s
    if (x in inter):
      scores.append(1.0/best)
  return scores