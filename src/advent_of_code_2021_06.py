"""
Lanternfish breed every 7 days. New lanternfish need 2 extra days for their first cycles.
Data is the days left to breed, from 0 to 8
Given the timings for each lanternfish, calculate how many there will be.
"""

import numpy as np

f = open("../data/input_20211206.txt", "r")
in_data = f.read()
f.close()

fish_ages = [int(a) for a in in_data.rstrip().split(",")]
fish_ages = np.array(fish_ages)

"""
Part 1:
How many lanternfish would there be after 80 days?

Part 2:
How many lanternfish would there be after 256 days?
"""
num_days = 256
# We only need to store the number of fish, not the fish themselves.

number_dict = {x: np.count_nonzero(fish_ages==x) for x in range(9)}

for day in range(num_days):
    # N1 becomes N0, N2 becomes N1, ..., N8 becomes N0
    # Exception: N6 is N0 + N7
    reproduced = number_dict[0]

    for i in range(8):
        number_dict[i] = number_dict[i+1]

    number_dict[6]+=reproduced
    number_dict[8]=reproduced

num_fish = 0

for k in number_dict.keys():
    num_fish+=number_dict[k]

print(num_fish)