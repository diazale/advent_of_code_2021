"""
Octopus flashing:
Each step increases energy level by 1 {0,...9}
When it reaches 9, it flashes, and all adjacent numbers flash too

At each step
1. Increase values by 1
2. Any >9 values flash
3. Any values adjacent to a >9 increase by 1; any 9s becomes 0s
Each octopus can only flash once per steps
"""

import numpy as np

f = open("../data/input_20211211.txt", "r")
in_data = f.read()
f.close()

octopi = np.array([list(d) for d in in_data.rstrip().split("\n")])
octopi = octopi.astype(int)

print(octopi, octopi.shape)

"""
Part 1:
How many flashes are there after 100 steps?

Part 2:
Find when all the octopi flash at the same time
"""

def increment(m_, r_, c_):
    """
    Increment the neighbours of a point in an array
    :param m_: Input matrix
    :param r_: row
    :param c_: column
    :return: returns a matrix of appropriate size with incremented neighbours
    """
    m_[r_,c_]-= 1 # Decrement flashpoint to account for increment
    temp_ = m_[max(0, r_ - 1):min(r_ + 2, m_.shape[0]), max(0, c_ - 1):min(c_ + 2, m_.shape[1])]
    temp_+= 1 # Increment neighbours

    return temp_

def neighbour_crawl(m_):
    """
    Recursive function that takes the octopus matrix.
    It goes cell-by-cell to check for coordinates with values > 9
    If there are, it increments and it adds it to the set of flashed coordinates and calls itself
    :param m_: Octopus matrix
    :return: Returns
    """
    for r_ in range(m_.shape[0]):
        for c_ in range(m_.shape[1]):
            if m_[r_,c_] > 9 and (r_,c_) not in flash_coords:
                # Add to coordinates visited
                flash_coords.add((r_,c_))

                # Increment neighbours if values is > 9
                m_[max(0, r_-1):min(r_+ 2,m_.shape[0]), max(0,c_-1):min(c_+2, m_.shape[1])] = increment(m_,r_,c_)

                return neighbour_crawl(m_)

    return m_

flashes = 0
sync = []
for step in range(1000):
    flash_coords = set()

    octopi+= 1
    octopi = neighbour_crawl(octopi)

    flashes+= len(flash_coords)

    print("After step", step+1, flashes, "total flashes")
    # Replace all >9 values with 0
    octopi[octopi>9]=0

    if np.all(octopi==0):
        sync.append(step+1)

    print(octopi)

print("Octopi synchronized at steps", sync)

