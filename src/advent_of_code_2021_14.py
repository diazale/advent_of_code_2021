"""
Polymerization

First line is a the polymer template (starting point)
Next lines are pair insertion rules
When AB -> appears, it means C should be inserted between A and B

All pairs are considered simultaneously and all insertions happen simultaneously within a step
Overlapping elements from neighbouring pairs are merged

e.g. NNC with rules {NN -> NCN, NC -> NBC} becomes NCNBC
"""
from collections import Counter

f = open("../data/input_20211214.txt", "r")
in_data = f.read()
f.close()

template = in_data.rstrip().split("\n\n")[0]
insertions = (in_data.rstrip().split("\n\n")[1]).split("\n")

insertion_rules = {}

for i in insertions:
    insertion_rules[i.split("->")[0].strip()] = i.split("->")[1].strip()

print(template)
print(insertion_rules)

"""
Part 1:
Apply ten steps of pair insertion and find the most/least common elements
Subtract the least common from the most common
"""

# Is there an opportunity to be clever here? Probably...
# Basic algo:
# 1. Split into all pairs
# 2. Apply rules
# 3. Create new polymer
# 4. GOTO 1

def get_pairs(template_):
    """
    Return a list of adjacent pairs in a given template

    :param template_: Polymer template
    :return: A list of pairs of elements
    """
    pairs_ = [template_[i_]+template_[i_+1] for i_ in range(len(template)-1)]
    return pairs_


#
# for step in range(2):
#     #print("Current template:", template)
#     pairs = get_pairs(list(template))
#     #print("Current pairs:", pairs)
#     cur_template = []
#     for p in range(len(pairs)):
#         #print(pairs[p], insertion_rules[pairs[p]], pairs[p][0]+insertion_rules[pairs[p]]+pairs[p][1])
#         if p < len(pairs)-1:
#             # Don't need to check the last element
#             cur_template.append(pairs[p][0]+insertion_rules[pairs[p]])
#         else:
#             cur_template.append(pairs[p][0]+insertion_rules[pairs[p]]+pairs[p][1])
#
#     #print("".join(cur_template))
#     template = "".join(cur_template)
#
#      #print(pairs[p], insertion_rules[pairs[p]], pairs[p][0]+insertion_rules[pairs[p]]+pairs[p][1])
#
# counts = Counter(template)
# print(counts.most_common()[0][1] - counts.most_common()[len(counts)-1][1])

"""
Part 2:
Do it after 40 steps. So uh, probably gonna need a better algorithm here.

Actually... All we need to know are the counts of the pairs and what they translate to
e.g. NNCB with rules {NN -> C, NC -> B, CB -> H} starts with NN=1, NC=1, CB=1
it then becomes NC++,CN++,NB++,BC++,CH++,HB++
the pairs present here become the keys for the next step
"""

# Step 1:
# Get the initial pairs
# Step 2:
# For each key in the counter dictionary:
# Increment the two associated pairs (or add them to the counter dict if they don't exist
# However, this only counts pairs. We want individual character counts

pair_counter = {k:0 for k in insertion_rules.keys()}
letter_counter = {l:0 for l in set("".join(list(insertion_rules.keys())))}
#print(pair_counter)

for step in range(40):
    # If this is the first, step, we initialize our pairs and counts
    if step==0:
        current_counter = pair_counter
        pairs = get_pairs(template)

        for l in list(template):
            # count the letter appearances
            # should be fine for initial set since it's short
            letter_counter[l]+= 1

        print("Initial letters", letter_counter)

        for pair in pairs:
            # These will be the counts for the next step
            current_counter[pair[0] + insertion_rules[pair]] += 1
            current_counter[insertion_rules[pair] + pair[1]] += 1
            letter_counter[insertion_rules[pair]] += 1

    else:
        for pair in current_counter.keys():
            if current_counter[pair] > 0:
                # For every pair that exists, increment the two pairs it creates by the times it appears
                pair_counter[pair[0] + insertion_rules[pair]] += current_counter[pair]
                pair_counter[insertion_rules[pair] + pair[1]] += current_counter[pair]
                letter_counter[insertion_rules[pair]] += current_counter[pair]

    current_counter = pair_counter #
    print("Step", step + 1, "pairs", current_counter)
    print("Step", step + 1, "letters", letter_counter)

    pair_counter = {k:0 for k in insertion_rules.keys()}

print(letter_counter[max(letter_counter, key=letter_counter.get)] - letter_counter[min(letter_counter, key=letter_counter.get)])