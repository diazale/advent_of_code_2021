"""
We're given a map of a subterranean cave stored as the connections between rooms
We have the start, the end, and two types of rooms
Those with capitals can be visited twice; those without, once
"""

from collections import defaultdict
import copy

f = open("../data/input_20211212.txt", "r")
#f = open("../data/test_input_20211212.txt", "r")
in_data = f.read()
f.close()

connections = [[d.split("-")[0],d.split("-")[1]] for d in in_data.rstrip().split("\n")]
#print(connections, len(connections))

#rooms = set()
rooms = set([d2 for d in in_data.rstrip().split("\n") for d2 in d.split("-")])

small_rooms = copy.deepcopy(rooms)

small_rooms.remove("start")
small_rooms.remove("end")

small_rooms = [r for r in small_rooms if r.lower()==r]

connection_dict = defaultdict(dict)

# Construct the matrix of connections
for r in rooms:
    for r2 in rooms:
        # Initialize room connections as 0
        connection_dict[r][r2] = 0

    for c in connections:
        #print(c)
        if r in c:
            #print(c[0], c[1])
            connection_dict[c[0]][c[1]] = 1
            connection_dict[c[1]][c[0]] = 1

print(connection_dict)

"""
Part 1:
Find all the paths, and find out how many start at "start", end at "end", and visit the small caves at most once
How many of these paths are there?
"""

# Probably recursive to find solutions, end when:
# 1. Hit end
# 2. Hit start (now cycling)
# 3. Hit small cave twice

# Can store data as a matrix? As a dict? As a set?
# If we store connections as a dict the algo is:
# 1. Start with the "start" element
# 2. Traverse the dictionary recursively
# 3. When we hit a small cave, drop it and its keys
# 4. If there is nowhere to go, exit
# 5. If we reach "start", exit
# 6. If we reach "end", add the path to a list and exit

def explore_caves(connections_, cave_, path_):
    """
    :param connections_: A dictionary/matrix representing valid connections
    :param cave_: The current room
    :param path_: The current path
    :return: If we reach the start or run out of rooms, terminate
    If we reach a small cave, make it unvisitable and explore its neighbours
    If we reach a large cave, explore its neighbours

    Maybe this should return a list for the path???
    """

    #print()
    #print("Entering cave", cave_)

    path_.append(cave_)
    #print("Current path:", path_)

    # First check if this is an end condition
    if cave_=="end":
        paths.append(list(path_))
        #print("***Finished mapping path:", path_)
    else:
        # Find connections from this cave
        neighbours = []
        for n in connections_[cave_]:
            if connections_[cave_][n]==1 and n!="start":
                # Don't add "start" as a valid neighbour
                neighbours.append(n)

        if len(neighbours)==0:
            # No valid neighbours: Exit
            #print("No valid neighbours")
            return

        #print("Neighbours:", neighbours)

        temp_connections_ = copy.deepcopy(connections_)
        for cur_cave in neighbours:
            # Explore each neighbouring cave
            # If we are currently in a small cave, remove connections to it from the graph
            #temp_connections_ = connections_.copy()
            temp_path_ = copy.deepcopy(path_)
            #if (cave_ not in ["start","end"]) and cave_.lower()==cave_:
            if cave_ in small_rooms:
                # Check if any small room has already been visited twice?
                for c_ in connections_:
                    connections_[c_][cave_] = 0

            #print("Leaving cave", cave_)
            #print("Using rules:", connections_[cur_cave])
            explore_caves(connections_, cur_cave, temp_path_)
            connections_ = copy.deepcopy(temp_connections_)
            #print("Returning to cave", cave_, "from", cur_cave)

paths = list()

# Start at "start" and explore the neighbours
#print("Starting dictionary:",connection_dict["start"])

explore_caves(connection_dict, "start", list())

#print(len(paths), paths)
print(len(paths))

"""
Part 2:
We can visit one small cave at most twice
How many paths are there now?
Run a check to see if a small room has been visited exactly once before
"""