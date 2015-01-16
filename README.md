# Evolutionary

Evolutionary algorithms applied to various types of problems.

1. Wargames - Contains a genetic algorithm to find the optimal allocation of resources in a simple wargame.

2. Prisoners - A simulation for Iterated Prisoner's Dilemma, a well known game theory problem. Genetic algorithm attempts to evolve an optimal strategy, which over a long enough timeline is Tit-for-Tat.

3. Traveling Salesman - Simulation to discover the shortest hamiltonian cycle on a set of 2d points. Runs 4 different genetic algorithms, a parametric optimizer that performs a stochastic hill climbing search, and a random search in an attempt to discover the optimal solution.

4. Symbolic Regression - Genetic program that evolves syntax trees representing mathematical formulas to fit a dataset of 2d points. Capable of learning functions involving binary operators (+,-,/,*) as well as unary operators (sin,cos,tan,sqrt). Runs 2 genetic simulations (1 with a special selection method called King of the Hill) as well as a a random search in an attempt to find the true function (if it exists, otherwise approximate).

## Running:

* Details on how to run the evolutionary algorithms are in running.txt file in
the respective folders.

## License:

* This project is licensed under the MIT open source license. Please see the LICENSE file for details.