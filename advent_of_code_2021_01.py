"""
To do this, count the number of times a depth measurement increases from the previous measurement.
(There is no measurement before the first measurement.)
"""

f = open("input_20211201.txt", "r")
in_data = f.read()
f.close()

# Read input; split by newline and drop empty line
depths = list(map(int,in_data.rstrip().split("\n")))
print(depths)


"""
Part 1: How many measurements are larger than the previous measurement?
"""
# Brute force: Loop and check neighbouring element
# Logical approach: subtract a shifted list from itself? Convert to numpy and count positive differences
import numpy as np
shifted_depths = depths.copy()
shifted_depths.pop(0)
shifted_depths.append(0) # Dummy element

depths = np.array(depths)
shifted_depths = np.array(shifted_depths)

diffs = shifted_depths[:-1] - depths[:-1] # Avoid dummy element

print(sum(diffs > 0)) # Positive value means an increase in depth

"""
Part 2: Compare the moving sums instead of single values
"""

# Use a sliding kernel
summed_depths = np.convolve(depths,np.ones(3,dtype=int),'valid')

shifted_summed_depths = summed_depths.copy()
shifted_summed_depths = shifted_summed_depths[1:]
shifted_summed_depths = np.append(shifted_summed_depths, 0)

print(summed_depths)
print(shifted_summed_depths)

diffs = shifted_summed_depths[:-1] - summed_depths[:-1]

print(sum(diffs > 0))