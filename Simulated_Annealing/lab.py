import json
import copy

import time

import numpy as np  # contains helpful math functions like numpy.exp()
import numpy.random as random  # see numpy.random module
# import random  # alternative to numpy.random module

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

"""Read input data and define helper functions for visualization."""

# Map services and data available from U.S. Geological Survey, National Geospatial Program.
# Please go to http://www.usgs.gov/visual-id/credit_usgs.html for further information
map = mpimg.imread("map.png")  # US States & Capitals map

# List of 30 US state capitals and corresponding coordinates on the map
with open('capitals.json', 'r') as capitals_file:
	capitals = json.load(capitals_file)
capitals_list = list(capitals.items())


def show_path(path, starting_city, w=12, h=8):
	"""Plot a TSP path overlaid on a map of the US States & their capitals."""
	x, y = list(zip(*path))
	_, (x0, y0) = starting_city
	plt.imshow(map)
	plt.plot(x0, y0, 'y*', markersize=15)  # y* = yellow star for starting point
	plt.plot(x + x[:1], y + y[:1])  # include the starting point at the end of path
	plt.axis("off")
	fig = plt.gcf()
	fig.set_size_inches([w, h])


def simulated_annealing(problem, schedule):
	"""The simulated annealing algorithm, a version of stochastic hill climbing
	where some downhill moves are allowed. Downhill moves are accepted readily
	early in the annealing schedule and then less often as time goes on. The
	schedule input determines the value of the temperature T as a function of
	time. [Norvig, AIMA Chapter 3]

	Parameters
	----------
	problem : Problem
		An optimization problem, already initialized to a random starting state.
		The Problem class interface must implement a callable method
		"successors()" which returns states in the neighborhood of the current
		state, and a callable function "get_value()" which returns a fitness
		score for the state. (See the `TravelingSalesmanProblem` class below
		for details.)

	schedule : callable
		A function mapping time to "temperature". "Time" is equivalent in this
		case to the number of loop iterations.

	Returns
	-------
	Problem
		An approximate solution state of the optimization problem

	Notes
	-----
		(1) DO NOT include the MAKE-NODE line from the AIMA pseudocode

		(2) Modify the termination condition to return when the temperature
		falls below some reasonable minimum value (e.g., 1e-10) rather than
		testing for exact equality to zero

	See Also
	--------
	AIMA simulated_annealing() pseudocode
		https://github.com/aimacode/aima-pseudocode/blob/master/md/Simulated-Annealing.md
	"""
	# raise NotImplementedError
	current = problem
	starttime = time.time()
	while True:
		temperature = schedule(time.time() - starttime)
		if temperature == 0 or temperature < 0.1:
			return current
		next = problem.successors()
		if len(next) > 0:
			next = np.random.choice(next, 1)[0]
		else:
			continue
		deltaE = next.get_value() - current.get_value()
		if deltaE > 0 or random.random() < (np.exp(deltaE / temperature)):
			current = next


class TravelingSalesmanProblem:
	"""Representation of a traveling salesman optimization problem.  The goal
	is to find the shortest path that visits every city in a closed loop path.

	Students should only need to implement or modify the successors() and
	get_values() methods.

	Parameters
	----------
	cities : list
		A list of cities specified by a tuple containing the name and the x, y
		location of the city on a grid. e.g., ("Atlanta", (585.6, 376.8))

	Attributes
	----------
	names
	coords
	path : list
		The current path between cities as specified by the order of the city
		tuples in the list.
	"""

	def __init__(self, cities):
		self.path = copy.deepcopy(cities)

	def copy(self):
		"""Return a copy of the current board state."""
		new_tsp = TravelingSalesmanProblem(self.path)
		return new_tsp

	@property
	def names(self):
		"""Strip and return only the city name from each element of the
		path list. For example,
			[("Atlanta", (585.6, 376.8)), ...] -> ["Atlanta", ...]
		"""
		names, _ = zip(*self.path)
		return names

	@property
	def coords(self):
		"""Strip the city name from each element of the path list and return
		a list of tuples containing only pairs of xy coordinates for the
		cities. For example,
			[("Atlanta", (585.6, 376.8)), ...] -> [(585.6, 376.8), ...]
		"""
		_, coords = zip(*self.path)
		return coords

	def successors(self):
		"""Return a list of states in the neighborhood of the current state by
		switching the order in which any adjacent pair of cities is visited.

		For example, if the current list of cities (i.e., the path) is [A, B, C, D]
		then the neighbors will include [A, B, D, C], [A, C, B, D], [B, A, C, D],
		and [D, B, C, A]. (The order of successors does not matter.)

		In general, a path of N cities will have N neighbors (note that path wraps
		around the end of the list between the first and last cities).

		Returns
		-------
		list<Problem>
			A list of TravelingSalesmanProblem instances initialized with their list
			of cities set to one of the neighboring permutations of cities in the
			present state
		"""
		# raise NotImplementedError
		neighbors = []
		for i in range(0, len(self.path)):
			new_path = copy.deepcopy(self.path)
			j = i + 1 if i + 1 < len(self.path) else 0
			new_path[i], new_path[j] = new_path[j], new_path[i]
			neighbors.append(TravelingSalesmanProblem(new_path))
		return neighbors

	def get_value(self):
		"""Calculate the total length of the closed-circuit path of the current
		state by summing the distance between every pair of adjacent cities.  Since
		the default simulated annealing algorithm seeks to maximize the objective
		function, return -1x the path length. (Multiplying by -1 makes the smallest
		path the smallest negative number, which is the maximum value.)

		Returns
		-------
		float
			A floating point value with the total cost of the path given by visiting
			the cities in the order according to the self.cities list

		Notes
		-----
			(1) Remember to include the edge from the last city back to the
			first city

			(2) Remember to multiply the path length by -1 so that simulated
			annealing finds the shortest path
		"""
		# raise NotImplementedError
		dist = 0.0
		for i in range(0, len(self.path)):
			j = i + 1 if i + 1 < len(self.path) else 0
			dist += ((self.path[i][1][0] - self.path[j][1][0]) ** 2 + (self.path[i][1][1] - self.path[j][1][1]) ** 2) \
			        ** 0.5
		return dist * -1


# Construct an instance of the TravelingSalesmanProblem
test_cities = [('DC', (11, 1)), ('SF', (0, 0)), ('PHX', (2, -3)), ('LA', (0, -4))]
tsp = TravelingSalesmanProblem(test_cities)
assert (tsp.path == test_cities)

# Test the successors() method -- no output means the test passed
successor_paths = [x.path for x in tsp.successors()]

assert (all(x in [[('LA', (0, -4)), ('SF', (0, 0)), ('PHX', (2, -3)), ('DC', (11, 1))],
                  [('SF', (0, 0)), ('DC', (11, 1)), ('PHX', (2, -3)), ('LA', (0, -4))],
                  [('DC', (11, 1)), ('PHX', (2, -3)), ('SF', (0, 0)), ('LA', (0, -4))],
                  [('DC', (11, 1)), ('SF', (0, 0)), ('LA', (0, -4)), ('PHX', (2, -3))]]
            for x in successor_paths))

# Test the get_value() method -- no output means the test passed
assert (np.allclose(tsp.get_value(), -28.97, atol=1e-3))

# These are presented as globals so that the signature of schedule()
# matches what is shown in the AIMA textbook; you could alternatively
# define them within the schedule function, use a closure to limit
# their scope, or define an object if you would prefer not to use
# global variables
alpha = 0.95
temperature = 1e4

def schedule(time):
	return temperature * (alpha ** time)

# test the schedule() function -- no output means that the tests passed
assert (np.allclose(alpha, 0.95, atol=1e-3))
assert (np.allclose(schedule(0), temperature, atol=1e-3))
assert (np.allclose(schedule(10), 5987.3694, atol=1e-3))

# Failure implies that the initial path of the test case has been changed
# assert(tsp.path == [('DC', (11, 1)), ('SF', (0, 0)), ('PHX', (2, -3)), ('LA', (0, -4))])
# result = simulated_annealing(tsp, schedule)
# print("Initial score: {}\nStarting Path: {!s}".format(tsp.get_value(), tsp.path))
# print("Final score: {}\nFinal Path: {!s}".format(result.get_value(), result.path))
# assert(tsp.path != result.path)
# assert(result.get_value() > tsp.get_value())

# Create the problem instance and plot the initial state
num_cities = 30
capitals_tsp = TravelingSalesmanProblem(capitals_list[:num_cities])
starting_city = capitals_list[0]
print("Initial path value: {:.2f}".format(-capitals_tsp.get_value()))
print(capitals_list[:num_cities])  # The start/end point is indicated with a yellow star
show_path(capitals_tsp.coords, starting_city)

alpha = 0.95
temperature=1e6
result = simulated_annealing(capitals_tsp, schedule)
print("Final path length: {:.2f}".format(-result.get_value()))
print(result.path)
show_path(result.coords, starting_city)