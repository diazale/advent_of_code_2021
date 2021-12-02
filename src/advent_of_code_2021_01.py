"""
To do this, count the number of times a depth measurement increases from the previous measurement.
(There is no measurement before the first measurement.)
"""

import numpy as np

f = open("../data/input_20211201.txt", "r")
in_data = f.read()
f.close()

# Read input; split by newline and drop empty line, and convert to numpy array
depths = np.array(list(map(int,in_data.rstrip().split("\n"))))

# Brute force: Loop and check neighbouring element
# Array approach: subtract a shifted list from itself. Positive values indicate an increase in previous measurement.

def shift(in_depths):
    """
    Function to shift a 1-D array by dropping the first element and padding with a 0 at the end.

    :param in_depths: Input array of depths
    :return: Array of depths shifted left by 1 with a dummy value of 0 appended to maintain array size
    """
    shifted = in_depths[1:]
    shifted = np.append(shifted, 0)

    return shifted

"""
Part 1: How many measurements are larger than the previous measurement?
"""

diffs = shift(depths)[:-1] - depths[:-1] # Avoid dummy element
print(sum(diffs > 0)) # Positive value means an increase in depth

"""
Part 2: Compare the moving sums instead of single values
"""

# Use a sliding kernel to sum the sliding 3-window
summed_depths = np.convolve(depths,np.ones(3,dtype=int),'valid')

diffs = shift(summed_depths)[:-1] - summed_depths[:-1]
print(sum(diffs > 0))