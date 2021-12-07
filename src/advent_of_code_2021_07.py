"""
Crab submarine positions are listed. Align the positions.
Moving 1 position costs 1 fuel.
"""

import numpy as np

f = open("../data/input_20211207.txt", "r")
in_data = f.read()
f.close()

positions = np.array([int(a) for a in in_data.rstrip().split(",")])

print(positions)

"""
Part 1:
Determine the horizontal position that the crabs can align to using the least fuel possible.
How much fuel must they spend to align to that position?
"""

# There's a maximum amount of fuel that can be spent (largest distance travelled)
# Brute force method: Loop from smallest to largest value and find the fuel expended for each one
# Then take the smallest

min_fuel_spent = np.sum(positions)

for u in list(set(positions)):

    fuel_spent = np.abs(positions - u)
    min_fuel_spent = min(np.sum(fuel_spent), np.sum(min_fuel_spent))

print(min_fuel_spent)

"""
Part 2:
Each step the submarine takes increments the fuel spent (e.g. 1->4 takes 1+2+3 fuel)
2->5 takes 1 + 2 + 3 as well
"""

# Find the difference and take the sum of integers up to the value
# So for each value, subtract position, and then at each position calculate the gaussian sum
min_fuel_spent = np.sum(positions)

def integer_sum(n):
    """
    Return the sum of integers up to and including n
    :param n: input integer
    :return: sum of integers using the Gaussian summation
    """
    return (n*(n+1))/2

min_fuel_spent = 99999999

for u in range(max(positions)):
    distances = np.apply_along_axis(integer_sum, 0, np.abs(positions - u))
    min_fuel_spent = min(np.sum(distances), min_fuel_spent)

print(min_fuel_spent)