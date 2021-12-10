"""
Lava tubes and heights

Smoke flows to the lowest level it's in. Input represents heights.

"""
import numpy as np

f = open("../data/input_20211209.txt", "r")
in_data = f.read()
f.close()

"""
Part 1:
Find all the low points (points that are less than those above/below/beside)
(diagonals do not count)
The risk level of a low point is its height. What is the sum of the risk levels?

Part 2: Find all the basins
Basins spread out from low points
"""

heights = [list(i) for i in in_data.rstrip().split("\n")]

heights = np.array(heights)
heights = heights.astype(int)


def peek(m_,r_,c_):
    """
    :param m_: Height matrix
    :param r_: row
    :param c_: column
    :return: returns the cell value, if it exists
    """
    # Note: numpy arrays don't handle -1 as an IndexError and instead return the last row/col
    if r_ in [-1,m_.shape[0]] or c_ in [-1,m_.shape[1]]:
        return 10
    else:
        return m_[r_,c_]

temp2 = []

def basin_crawl(m_,r_,c_):
    """
    Recursive function to check points for basins
    :param m_: Height matrix
    :param r_: row
    :param c_: column
    :return: a list of the [r_,c_] values
    """

    # Peek left
    if m_[r_,c_] < peek(m_,r_,c_-1) < 9:
        basin_crawl(m_,r_,c_-1)
    # Peek up
    if m_[r_,c_] < peek(m_,r_-1,c_) < 9:
        basin_crawl(m_,r_-1,c_)
    # Peek right
    if m_[r_,c_] < peek(m_,r_,c_+1) < 9:
        basin_crawl(m_,r_,c_+1)
    # Peek down
    if m_[r_,c_] < peek(m_,r_+1,c_) < 9:
        basin_crawl(m_,r_+1,c_)

    basins[str(r)+","+str(c)].append([r_,c_])
    return [r_,c_]

basins = {}
low_points = []

for r in range(heights.shape[0]):
    for c in range(heights.shape[1]):
        if heights[r,c] < min(peek(heights,r+1,c), peek(heights,r-1,c), peek(heights,r,c+1), peek(heights,r,c-1)):
            # Get low points
            low_points.append(heights[r, c])

            # Use the low point as the key for this basin
            basins[str(r) + "," + str(c)]=[]

            # Recursively create a list of points belonging to the basin
            basin_crawl(heights,r,c)

            # Remove duplicate points in the basin
            basins[str(r) + "," + str(c)] = [list(b) for b in set(tuple(b) for b in basins[str(r) + "," + str(c)])]

print(np.sum(np.array(low_points)+1))

sizes = []

for k in basins.keys():
    sizes.append(len(basins[k]))

print(np.prod(np.array(sorted(sizes, reverse=True)[:3])))