Evolutionary
============

Evolutionary algorithms applied to various types of problems.

- Wargames - Contains a genetic algorithm to find the optimal allocation of resources in a simple wargame.

- Prisoners - A simulation for Iterated Prisoner's Dilemma, a well known game theory problem. Genetic algorithm attempts to evolve an optimal strategy, which over a long enough timeline is Tit-for-Tat.

- Traveling Salesman - Simulation to discover the shortest hamiltonian cycle on a set of 2d points. Runs 4 different genetic algorithms, a parametric optimizer that performs a stochastic hill climbing search, and a random search in an attempt to discover the optimal solution.

- Symbolic Regression - Genetic program that evolves syntax trees representing mathematical formulas to fit a dataset of 2d points. Capable of learning functions involving binary operators (+,-,/,*) as well as unary operators (sin,cos,tan,sqrt). Runs 2 genetic simulations (1 with a special selection method called King of the Hill) as well as a a random search in an attempt to find the true function (if it exists, otherwise approximate).
