# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?
A: The idea of naked twins is to find the two boxes within the same unit that have the exact same two possible values. Then we know the two possible values could only be in these two boxes and no boxes in the same unit could have these two possible values. Because of that, we could eliminate the two possible values from other boxes in the same unit and simplify the puzzle.
This technique should be combined with other methods like eliminate and only choice as constraint propagation to simplify the puzzle by reducing the search space.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?
A: Compare to the normal sudoku problem, the diagonal sudoku problem introduced another constraint which is: among the two main diagonals, the numbers 1 to 9 should all appear exactly once. Thus boxes on the two main diagonals will have new peers and constraint. When we construct the units, we need to have two diagonal unit in addition to the row units, column units and square units.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project.
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
