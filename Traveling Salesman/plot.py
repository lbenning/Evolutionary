import matplotlib.pyplot as plt
from tools import errorBars

'''
Plots resulting path lengths found over time by the genetic algorithms 
and parametric optimizers
'''

# Plot results : Path Length vs. Number of Evaluations
def graph(genPmx,genHalf,stoch,rand,intervals):

	# Compute error bars for each simulation
	genPmxErrors = errorBars(genPmx,intervals)
	genHalfErrors = errorBars(genHalf,intervals)
	stochErrors = errorBars(stoch,intervals)
	randErrors = errorBars(rand,intervals)

	# Average simulation results
	genPmxColl = collapse(genPmx)
	genHalfColl = collapse(genHalf)
	stochColl = collapse(stoch)
	randColl = collapse(rand)

	# Plot averaged fitness values
	plt.plot(intervals,genPmxColl,"red",
		intervals,genHalfColl,"blue",
		intervals,stochColl,"green",
		intervals,randColl,"purple")

	plt.ylabel('Path Length')
	plt.xlabel('Evaluations')
	plt.title('Travelling Salesman Path Lengths')

	# Plot error bars
	for x in range(len(intervals)):
		plt.errorbar(intervals[x], genPmxColl[x], yerr=genPmxErrors[x],
		 linestyle="None", marker="None", color="red")
		plt.errorbar(intervals[x], genHalfColl[x], yerr=genHalfErrors[x],
		 linestyle="None", marker="None", color="blue")
		plt.errorbar(intervals[x], stochColl[x], yerr=stochErrors[x],
		 linestyle="None", marker="None", color="green")
		plt.errorbar(intervals[x], randColl[x], yerr=randErrors[x],
		 linestyle="None", marker="None", color="purple")

	# Display the plot - woohoo!
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