# Monte Carlo Tree Search, Alpha-Beta Pruning, and Minimax Algorithms in Checkers

###### Required Packages
This code is implemented in Python and requires the random and NumPy packages.

###### Checkers Implementation
The game of checkers was implemented using a 6x6 NumPy array which represents the playing board. The rules of the game are enforced through variables and functions in the Board.py file. 

###### Monte Carlo Tree Search Algorithm Implementation
This implementation of the Monte Carlo Tree Search (MCTS) algorithm uses the upper confidence bound, or UCB1, formula given by  $UCB1 = V_i + 2 \sqrt{ln(N) / n_i}$  where $V_i$ is the average value of all nodes beneath the current node, $N$ is the number of times the parent node has been visited, and $n_i$ is the number of times child $i$ of the current node has been visited.

###### Results
After testing the MCTS agent against all other agents (Alpha-Beta and Minimax), the MCTS agent emerged victorious 100% of the time.
