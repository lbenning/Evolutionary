import matplotlib.pyplot as plt
from tools import errorBars

'''
Plots resulting path lengths found over time by the genetic algorithms 
and parametric optimizers
'''

# Plot results : Path Length vs. Number of Evaluations
def graph(pgtr,pgrr,hgr,hgrr,rr,sr,intervals):

	pg = errorBars(pgtr,intervals)
	pr = errorBars(pgrr,intervals)
	hg = errorBars(hgr,intervals)
	hr = errorBars(hgrr,intervals)
	st = errorBars(sr,intervals)
	ra = errorBars(rr,intervals)

	pgcoll = collapse(pgtr)
	prcoll = collapse(pgrr)
	hgcoll = collapse(hgr)
	hrcoll = collapse(hgrr)
	stcoll = collapse(sr)
	racoll = collapse(rr)

	plt.plot(intervals,pgcoll,"red",
		intervals,prcoll,"blue",
		intervals,hgcoll,"green",
		intervals,hrcoll,"purple",
		intervals,stcoll,"black",
		intervals,racoll,"orange")

	plt.ylabel('Path Length')
	plt.xlabel('Evaluations')
	plt.title('Travelling Salesman Path Lengths')

	for x in range(len(pg)):
		plt.errorbar(intervals[x], pgcoll[x], yerr=pg[x], linestyle="None", marker="None", color="red")
		plt.errorbar(intervals[x], prcoll[x], yerr=pr[x], linestyle="None", marker="None", color="blue")
		plt.errorbar(intervals[x], hgcoll[x], yerr=hg[x], linestyle="None", marker="None", color="green")
		plt.errorbar(intervals[x], hrcoll[x], yerr=hr[x], linestyle="None", marker="None", color="purple")
		plt.errorbar(intervals[x], stcoll[x], yerr=st[x], linestyle="None", marker="None", color="black")
		plt.errorbar(intervals[x], racoll[x], yerr=ra[x], linestyle="None", marker="None", color="orange")

	plt.show()

# Average together path scores of the same algorithm
def collapse(pgtr):
	t = []
	for x in range(len(pgtr[0])):
		tot = 0.0
		for y in range(len(pgtr)):
			tot += pgtr[y][x]
		t.append(tot/len(pgtr))
	return t