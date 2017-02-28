import pprint
import copy

from utils import *


def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    # pprint.pprint(solved_values)
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values


def only_choice(values):
    for unit in unitlist:
        # pprint.pprint('=========unit=========')
        # pprint.pprint(unit)
        for digit in '123456789':
            dplace = [box for box in unit if digit in values[box]]
            # pprint.pprint('=========dplace=========' + digit)
            # pprint.pprint(dplace)
            if len(dplace) == 1:
                values[dplace[0]] = digit
                # pprint.pprint('=========got only choice=========')
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len(
            [box for box in values.keys() if len(values[box]) == 1])
        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len(
            [box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available
        # values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    #"Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values == False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        # pprint.pprint(values)
        return values  # Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    min_poss = 9
    choosen_box = 0
    poss_values = []
    answers = []
    flag = False
    for box in values.keys():
        poss = len(values[box])
        if poss > 1 and poss < min_poss:
            choosen_box = box
            min_poss = poss
    # pprint.pprint(choosen_box + ': ' + str(min_poss) +
    #               ' - ' + str(values[choosen_box]))
    for digit in values[choosen_box]:
        tmp = copy.deepcopy(values)
        tmp[choosen_box] = digit
        poss_values.append(tmp)

    # Now use recursion to solve each one of the resulting sudokus, and if one
    for poss_value in poss_values:
        tmp = search(poss_value)
        if tmp:
            flag = True
            values = tmp
            break

    if flag == True:
        return values
    else:
        return False

pprint.pprint(search(grid_values(grid2)))

# reduce_puzzle(grid_values(grid))
# pprint.pprint(reduce_puzzle(grid_values(grid)))

# only_choice(grid_values(grid))
# pprint.pprint(only_choice(grid_values(grid)))

# pprint.pprint(eliminate(grid_values(grid)))
# pprint.pprint(eliminate(eliminate(grid_values(grid))))
