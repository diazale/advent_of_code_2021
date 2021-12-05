"""
Hydrothermal vents are laid out in lines given by coordinates in the format x1,y1 -> x2,y2
e.g 905,103 -> 905,82

An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.
"""

from collections import Counter
import numpy as np

f = open("../data/input_20211205.txt", "r")
in_data = f.read()
f.close()

lines = in_data.rstrip().split("\n")

# Filter out diagonal lines, so either x1 = x2 or y1 = y2
coord_pairs = list()
for line in lines:
    temp = line.split("->")
    coord_pairs.append([tuple([int(c) for c in temp[0].split(",")]), tuple([int(c) for c in temp[1].split(",")])])

"""
Part 1
Consider only horizontal and vertical lines (either x1=x2 or y1=y2).
At how many points do at least two lines overlap?
Note: WLOG, x2 can be smaller than x1
"""

# A horizontal line exists whenever y1=y2; vertical when x1=x2
# Mark the coordinates between these points (inclusive)
# Count the unique non-unique elements in the list of coordinates visited
coords_visited = list()

# List all points visited by a line
for c in coord_pairs:
    # Only consider horizontal or vertical lines
    x1, x2, y1, y2 = c[0][0], c[1][0], c[0][1], c[1][1]
    if x1==x2:
        coords_visited += [(x1, y) for y in range(min(y1,y2), max(y1,y2) + 1)]
    elif y1==y2:
        coords_visited += [(x, y1) for x in range(min(x1,x2), max(x1,x2) + 1)]

coords_counted = Counter(coords_visited)

temp = [x for x, count in coords_counted.items() if count > 1]
print(len(temp))

"""
Part 2
Consider 45-degree diagonal lines as well (the only valid diagonal lines)
"""

# Two types of diagonal lines: negative and positive slope
# so m= +/-1 (y = mx + b)
# Negative slope decreases y as x increases
# Positive slope increases y as x increases

coords_visited = list()

def slope(x1_,x2_,y1_,y2_):
    """
    Return the slope of a line
    :param x1_: x1
    :param x2_: x2
    :param y1_: y1
    :param y2_: y2
    :return: delta y over delta x. Will only ever be +/-1 because it's a 45 degree line.
    """
    m_ = (y2_-y1_)/(x2_-x1_)
    return m_

temp = 0

# List all points visited by a line
for c in coord_pairs:
    x1, x2, y1, y2 = c[0][0], c[1][0], c[0][1], c[1][1]
    if x1==x2:
        # Vertical
        coords_visited += [(x1, y) for y in range(min(y1,y2), max(y1,y2) + 1)]
    elif y1==y2:
        # Horizontal
        coords_visited += [(x, y1) for x in range(min(x1,x2), max(x1,x2) + 1)]
    else:
        # Diagonal
        # Start at minimum x and associated y and increase/decrease y based on m
        m = slope(x1,x2,y1,y2)

        if x1 < x2:
            y = y1
            for x in range(x1,x2 + 1):
                coords_visited.append(tuple([x, y]))
                y+=int(m)
        elif x2 < x1:
            y = y2
            for x in range(x2,x1 + 1):
                coords_visited.append(tuple([x, y]))
                y+=int(m)

coords_counted = Counter(coords_visited)

temp = [x for x, count in coords_counted.items() if count > 1]
print(len(temp))