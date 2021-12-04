"""
We have a list of bingo numbers being called and a collection of bingo cards
"""

import numpy as np

f = open("../data/input_20211204.txt", "r")
in_data = f.read()
f.close()

# Input data. This took too much thought.
# Get the list of numbers
numbers = [int(n) for n in in_data.rstrip().split("\n")[0].split(",")]
print(numbers)
print()

# Get the cards
# Cards are 5x5 space-delimited elements separated by double-newlines
cards = list()

for c in in_data.split("\n")[2:]:
    if len(c) > 0:
        cards.append([int(c_) for c_ in c.split()])

cards = np.array(cards)

# Cast the bingo cards into a 3d array of 5x5 2d arrays
cards = cards.reshape(int(len(cards)/5), -1, cards.shape[-1])
#print(cards, type(cards), cards.shape)

"""
Part 1:
Go through the list of numbers and mark the cards
When there is a complete row or column, a card is a winner
Figure out which card is the first winner
Then sum the winning card's uncalled numbers and multiply by the final number
"""

# Initialize a boolean matrix of equal dimension to the card matrix
indicator_matrix = np.zeros(cards.shape)

# Check sums along axis 1 and 2 (axis 0 is the card index, 1 is column, 2 is row)
# If any row or column in a card sums to 5, we have a winner and note its index
for n in numbers:
    indicator_matrix[cards==n]=1

    col_sums = np.sum(indicator_matrix, axis=1)
    row_sums = np.sum(indicator_matrix, axis=2)
    if 5 in col_sums or 5 in row_sums:
        print("A winner is you!")
        if 5 in col_sums:
            print("It's a column!")
            winner_idx = np.where(col_sums == 5)[0]
            print(np.where(col_sums == 5))
        else:
            print("It's a row!")
            winner_idx = np.where(row_sums == 5)[0]
            print(np.where(row_sums == 5))

        break

print(indicator_matrix[winner_idx,:,:])
print(cards[winner_idx,:,:], n)

uncalled = np.multiply(np.logical_not(indicator_matrix[winner_idx,:,:]), cards[winner_idx,:,:])
print(np.concatenate(uncalled).sum()*n)

"""
Part 2:
Same as before, but figure out which board will be the last to win
"""

# Initialize a boolean matrix of equal dimension to the card matrix
indicator_matrix = np.zeros(cards.shape)

# Check sums along axis 1 and 2 (axis 0 is the card index, 1 is column, 2 is row)
# Once a card is a winner, we could remove it from the array entirely
for n in numbers:
    indicator_matrix[cards==n]=1

    col_sums = np.sum(indicator_matrix, axis=1)
    row_sums = np.sum(indicator_matrix, axis=2)
    if 5 in col_sums or 5 in row_sums:
        print("A winner is you!")
        if 5 in col_sums:
            print("It's a column!")
            winner_idx = np.where(col_sums == 5)[0]
            print(np.where(col_sums == 5))
        else:
            print("It's a row!")
            winner_idx = np.where(row_sums == 5)[0]
            print(np.where(row_sums == 5))

        # Check if this is the last card
        if indicator_matrix.shape[0] > 1:
            # Once a card is a winner, delete it
            indicator_matrix = np.delete(indicator_matrix, winner_idx, 0)
            cards = np.delete(cards, winner_idx, 0)
        else:
            uncalled = np.multiply(np.logical_not(indicator_matrix[winner_idx, :, :]), cards[winner_idx, :, :])
            print(uncalled)
            print(np.concatenate(uncalled).sum() * n)
            break