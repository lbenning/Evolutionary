#! /usr/bin/python

from genetic import genetic
from parametric import stochClimb
from parametric import randSearch
from tools import getData
from plot import graph
import sys
from threading import Thread

global data
global evaluations
global intervals

global pgtr # PMX Variation, Top 40% Selection
global pgrr # PMX Variation, Roulette Selection
global hgr # Half + Reorder Variation, Top 40% Selection
global hgrr # Half + Reorder Variation, Roulette Selection
global rr # Random search over path
global sr # Stochastic hill climbing search with restarts

def pgen():
	pgtr.append(genetic(data, evaluations, intervals, False, True))

def prgen():
	pgrr.append(genetic(data, evaluations, intervals, False, False))

def hgen():
	hgr.append(genetic(data, evaluations, intervals, True, True))

def hrgen():
	hgrr.append(genetic(data, evaluations, intervals, True, False))

def stoch():
	sr.append(stochClimb(data, evaluations, intervals))
	
def rand():
	rr.append(randSearch(data, evaluations, intervals))

def main(name,iterations,eva,count):

	global data
	global evaluations
	global intervals

	global pgtr
	pgtr = []
	global rr
	rr = []
	global sr
	sr= []
	global hgr
	hgr = []
	global pgrr
	pgrr = []
	global hgrr
	hgrr = []

	data = getData(name)	
	intervals = []
	intervals.append(1)
	for x in range(1,count+1):
		intervals.append(x*(eva/count))
	evaluations = eva

	for x in range(iterations):
		t=Thread(target=pgen)
		s=Thread(target=stoch)
		u=Thread(target=rand)
		v=Thread(target=hgen)
		q=Thread(target=prgen)
		w=Thread(target=hrgen)
		t.start()
		s.start()
		u.start()
		v.start()
		q.start()
		w.start()
		t.join()
		s.join()
		u.join()
		v.join()
		q.join()
		w.join()

	graph(pgtr,pgrr,hgr,hgrr,rr,sr,intervals)

'''
arg1 : Filename to read in list of 2d points
arg2 : Number of iterations n > 0
arg3 : Number of evaluations m > 0
arg4 : Number of interval points to plot i > 0 (in addition to 1)
'''
if __name__ == '__main__':
    main(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]))