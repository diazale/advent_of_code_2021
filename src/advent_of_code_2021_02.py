"""
Given a list of movements (backward or up/down and a value)
"""

f = open("../data/input_20211202.txt", "r")
in_data = f.read()
f.close()

# Read input; split by newline and drop empty line, and convert to numpy array
directions = list(in_data.rstrip().split("\n"))

# The submarine starts at coordinate (0,0)
# Need to parse each input for direction and distance
def parse(d_):
    """
    Parse input for direction and distance
    :param d_: in_direction (e.g. "forward 7")
    :return: two values (direction, distance)
    """

    return d_.split()[0], int(d_.split()[1])


"""
Part 1: What do you get if you multiply your final horizontal position by your final depth?
"""

horizontal = 0
depth = 0

for d in directions:
    direction, distance = parse(d)

    if direction=="forward":
        horizontal+=distance
    elif direction=="up":
        depth-=distance
    elif direction=="down":
        depth+=distance

print(horizontal*depth)

"""
Part 2

In addition to horizontal position and depth, you'll also need to track a third value, aim, which also starts at 0. 
The commands also mean something entirely different than you first thought:
-down X increases your aim by X units.
-up X decreases your aim by X units.
-forward X does two things:
--It increases your horizontal position by X units.
--It increases your depth by your aim multiplied by X.

What do you get if you multiply your final horizontal position by your final depth?
"""

aim = 0
horizontal = 0
depth = 0

for d in directions:
    direction, distance = parse(d)

    if direction=="down":
        aim+=distance
    elif direction=="up":
        aim-=distance
    elif direction=="forward":
        horizontal+=distance
        depth+=aim*distance

print(horizontal*depth)