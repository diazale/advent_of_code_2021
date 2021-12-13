"""

Input is a set of coordinates (dots) for paper
At the bottom there are folding instructions

Paper is transparent, so dots (#) overwrite blanks (.)
Paper is folded UP (along y=...) or LEFT (along x=...)
"""
import numpy as np

#f = open("../data/test_input_20211213.txt", "r")
f = open("../data/input_20211213.txt", "r")
in_data = f.read()
f.close()

coordinates, instructions = in_data.rstrip().split("\n\n")

coordinates = [[int(x.split(",")[0]), int(x.split(",")[1])] for x in coordinates.split("\n")]

print(coordinates)
instructions = instructions.split("\n")
print(instructions)

# Might be useful to represent dots as 1 and empty spots as 0, so overwriting an empty spot is just
# coord[1] + coord[2]; empty spots remain 0, otherwise non-zero

"""
Part 1:
How many dots are visible after doing the first fold instruction?
"""

# Find the dimensions of the matrix
max_cols = max([c[0] for c in coordinates])
max_rows = max([c[1] for c in coordinates])

# Populate the matrix
coordinate_matrix = np.zeros([max_rows+1, max_cols+1])

cols = [c[0] for c in coordinates]
rows = [c[1] for c in coordinates]

coordinate_matrix[rows,cols]+= 1

print(coordinate_matrix)
print(coordinate_matrix.shape)

# Fold along instruction line
# y = Y means fold up along row Y
# Everything below row Y is flipped and added to everything above row Y
new_matrix = coordinate_matrix
count = 0
for i in instructions:
    # Get the fold line
    fold_line = int(i.split("=")[1])
    print(i)
    if i.split("=")[0][-1]=="y":
        # Fold up
        # Split the matrix along row y
        top = new_matrix[:fold_line,:]
        bot = new_matrix[fold_line+1:,:]
        bot_flipped = np.flip(bot, 0)

        print("Top starting shape:", top.shape)
        print("Bot starting shape:", bot_flipped.shape)

        # If the top matrix is bigger, pad the flipped version with rows of zeroes on the top
        if top.shape[0] > bot_flipped.shape[0]:
            bot_flipped = np.r_[np.zeros([abs(top.shape[0] - bot_flipped.shape[0]), bot_flipped.shape[1]]), bot_flipped]

        print("Top padded shape:", top.shape)
        print("Bot padded shape:", bot_flipped.shape)
        new_matrix = top + bot_flipped
    elif i.split("=")[0][-1]=="x":
        # Fold left
        # Split matrix along col x
        left = new_matrix[:,:fold_line]
        right = new_matrix[:,fold_line+1:]

        right_flipped = np.flip(right, 1)

        print("Left starting shape:", left.shape)
        print("Right starting shape:", right_flipped.shape)

        # If the left matrix is bigger, pad the flipped right matrix with columns of zeroes on the left side
        if left.shape[1] > right_flipped.shape[1]:
            right_flipped = np.c_[np.zeros([right_flipped.shape[0], 1]), right_flipped]

        print("Left padded shape:", left.shape)
        print("Right padded shape:", right_flipped.shape)

        new_matrix = left + right_flipped

    count+=1

    #if count > 1:
        # Part 1
    #    print(np.sum(new_matrix > 0))
    #    break

"""
Part 2:
Carry out all the instructions and find the 8-letter code
"""

for row in range(new_matrix.shape[0]):
    temp = []
    for t in new_matrix[row,:]:
        if t > 1:
            temp.append("#")
        else:
            temp.append(".")

    print("".join(temp))