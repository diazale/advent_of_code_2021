"""
Given a list of binary inputs
"""
import numpy as np

f = open("../data/input_20211203.txt", "r")
in_data = f.read()
f.close()

diagnostics = in_data.rstrip().split("\n")

# We want to get the data into a binary matrix form
diagnostics_matrix = list()

for d in diagnostics:
    diagnostics_matrix.append([int(d1) for d1 in d])

diagnostics_matrix = np.array(diagnostics_matrix)

"""
Part 1:
Find the most common value per bit and concatenate (gamma rate)
Find the least common per bit and concatenate (epsilon rate)
Multiply the decimal value of each and return the decimal value
"""

# The gamma rate is 1 if the most common value in a column is 1 and 0 otherwise
# This is logically equivalent to rounding the mean value of a column
# Column mean > 0.5 => gamma rate of 1
# Column mean < 0.5 => gamma rate of 0
# The epsilon rate is the element-wise logical inverse of the gamma rate
gamma_rate = np.round_(diagnostics_matrix.sum(axis=0)/diagnostics_matrix.shape[0],0)
epsilon_rate = np.float64(np.logical_not(gamma_rate))

gamma_rate = int("".join([str(int(g)) for g in gamma_rate]),2)
epsilon_rate = int("".join([str(int(e)) for e in epsilon_rate]),2)

print(gamma_rate * epsilon_rate)

"""
Part 2:
Verify the life support rating
Determined by multiplying the oxygen generator rating by the CO2 scrubber rating.

Start with the full list of binary numbers from your diagnostic report and consider just the first bit of those numbers.
Then:

Keep only numbers selected by the bit criteria for the type of rating value for which you are searching.
Discard numbers which do not match the bit criteria.
If you only have one number left, stop; this is the rating value for which you are searching.
Otherwise, repeat the process, considering the next bit to the right.

To find oxygen generator rating, determine the most common value (0 or 1) in the current bit position, 
and keep only numbers with that bit in that position. 
If 0 and 1 are equally common, keep values with a 1 in the position being considered.

To find CO2 scrubber rating, determine the least common value (0 or 1) in the current bit position, 
and keep only numbers with that bit in that position. 
If 0 and 1 are equally common, keep values with a 0 in the position being considered.
"""

# Find the gamma rate for the first column, and drop every row that doesn't match
# Then do this for the second, third, etc, columns

def gamma_epsilon(m_):
    """
    Return the gamma and epsilon rate vectors for a given binary matrix

    :param m_: a binary matrix
    :return: vectors of the most and least common values per position
    """

    # If the mean is 0.5, replace it with a 1
    # Otherwise, carry out with rounding as before.
    g_ = m_.sum(axis=0) / m_.shape[0]
    g_ = np.round_(np.where(g_==0.5, 1, g_), 0)

    # Epsilon rate is still the element-wise logical inverse
    e_ = np.float64(np.logical_not(g_))

    return g_, e_

# Strategy:
# Create an oxygen and CO2 copy of the diagnostics matrix
# Iterating through columns, find the gamma and epsilon values
# Use these values to create a boolean vector of which rows to keep/drop
# Keep/drop rows accordingly
oxygen_matrix = diagnostics_matrix
co2_matrix = diagnostics_matrix

for c in range(0,diagnostics_matrix.shape[1]):
    if oxygen_matrix.shape[0] > 1:
        gamma_o2, epsilon_o2 = gamma_epsilon(oxygen_matrix)
        oxygen_matrix = oxygen_matrix[oxygen_matrix[:,c]==gamma_o2[c],:]

        if oxygen_matrix.shape[0]==1:
            oxygen_rate = oxygen_matrix.flatten()
            print("Oxygen rate determined! On iteration:", c, "Rate:", oxygen_rate)

    if co2_matrix.shape[0] > 1:
        gamma_co2, epsilon_co2 = gamma_epsilon(co2_matrix)
        co2_matrix = co2_matrix[co2_matrix[:,c]==epsilon_co2[c],:]

        if co2_matrix.shape[0]==1:
            co2_rate = co2_matrix.flatten()
            print("CO2 rate determined! On iteration:", c, "Rate:", co2_rate)

# Convert the values to decimal
oxygen_rate = int("".join([str(int(o)) for o in oxygen_rate]),2)
co2_rate = int("".join([str(int(c)) for c in co2_rate]),2)

print(oxygen_rate*co2_rate)
