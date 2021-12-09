"""
Input is some sort of code to represent 7-line numbers represented by letters a through g

 aaaa
b    c
b    c
 dddd
e    f
e    f
 gggg

Segment signals have been scrambled, e.g. we might get "bg" but that just means two letters are activated,
and the only number with two letters is 1 ("cf"), so the number is actually 1
"""

f = open("../data/input_20211208.txt", "r")
in_data = f.read()
f.close()

"""
Part 1:
Figure out the easy numbers in the output: How often to 1, 4, 7, 8 appear?
"""

output_values = [i.split("|")[1].strip().split() for i in in_data.rstrip().split("\n")]
#print(output_values)

# 1 has two letters, 4 has four, 7 has three, 8 has seven
# Count the output values with those lengths
count = 0

for o in output_values:
    for letters in o:
        if len(letters) in [2,3,4,7]:
            count+=1

#print(count)

"""
Part 2:
For each entry, determine all of the wire/segment connections and decode the four-digit output values.
What do you get if you add up all of the output values?

So for the first line, we have:
cdafg dage fgdaec cdbfgae cge gcbdfa fdceb gfceab ge ecfgd | eg eg dfecag ge

We can find the values of 1, 4, 7, and 8, which will give us the other numbers
1 -- maps the two right segments
4 -- maps the top-left and middle segments
7 -- maps the top and two right segments
8 -- maps all segments

Segments used:
2: 1
3: 7
4: 4
5: 2,3,5
6: 0,6,9
7: 8

How do we distinguish between 2,3,5?
-2 has one segment in common with 0,6,8
-3 has two segments in common with 0,1,4,7,8,9
-5 has one segment in common with 0,4,6,8,9

How do we distinguish between 6,9?
-0 contains 1,7 fully
-6 contains 5 fully
-9 contains 1,3,4,7 fully

Can we express each digit as a set of other digits?
"""


input_segments = [i.split("|")[0].strip().split() for i in in_data.rstrip().split("\n")]
output_segments = [i.split("|")[1].strip().split() for i in in_data.rstrip().split("\n")]

# Order of characters doesn't matter, so sort them for simplicity
input_segments_sorted = []
output_segments_sorted = []

for n in range(len(input_segments)):
    temp = []
    for i in input_segments[n]:
        temp.append("".join(sorted(i)))

    input_segments_sorted.append(temp)

    temp = []
    for o in output_segments[n]:
        temp.append("".join(sorted(o)))

    output_segments_sorted.append(temp)

print(input_segments_sorted)

sum_val = 0

# Note: letter order doesn't matter, just the elements themselves matter
for n in range(len(input_segments_sorted)):
    segment_dict = {}

    while len(segment_dict) < 10:
        # Identify easy numbers first
        for i in input_segments_sorted[n]:
            if len(i)==2:
                segment_dict["1"] = i
            elif len(i)==3:
                segment_dict["7"] = i
            elif len(i)==4:
                segment_dict["4"] = i
            elif len(i)==7:
                segment_dict["8"] = i

        if "9" not in segment_dict.keys():
            # 9 is the only length 6 number than contains 4
            for i in input_segments_sorted[n]:
                if len(i)==6:
                    if set(segment_dict["4"]) == set(segment_dict["4"]).intersection(set(i)):
                        segment_dict["9"] = i

        if "3" not in segment_dict.keys():
            # 3 is the only length 5 number than contains 1
            for i in input_segments_sorted[n]:
                if len(i)==5:
                    if set(segment_dict["1"]) == set(segment_dict["1"]).intersection(set(i)):
                        segment_dict["3"] = i

        if "0" not in segment_dict.keys():
            if "3" in segment_dict.keys():
                # 0 is the only length 6 number that contains 1 and the left bar (8-3)
                left_bar = set(segment_dict["8"]) - set(segment_dict["3"])

                for i in input_segments_sorted[n]:
                    if len(i)==6:
                        if set(i) == set(i) | set(segment_dict["1"]) | left_bar:
                            segment_dict["0"] = i

        if ("6" not in segment_dict.keys()) and "0" in segment_dict.keys() and "9" in segment_dict.keys():
            # If we have 0 and 9 we can find 6 as the remaining length 6 code
            for i in input_segments_sorted[n]:
                if len(i)==6:
                    if set(i)!=set(segment_dict["0"]) and set(i)!=set(segment_dict["9"]):
                        segment_dict["6"] = i

        if ("5" not in segment_dict.keys()) and "6" in segment_dict.keys():
            for i in input_segments_sorted[n]:
                # 5 is contained completely within 6
                if len(i)==5 and set(i) == set(i).intersection(set(segment_dict["6"])):
                    segment_dict["5"] = i

        if ("2" not in segment_dict.keys()) and "3" in segment_dict.keys() and "5" in segment_dict.keys():
            # The last remaining length 5 code must be 2
            for i in input_segments_sorted[n]:
                if len(i)==5:
                    if set(i)!=set(segment_dict["3"]) and set(i)!=set(segment_dict["5"]):
                        segment_dict["2"] = i


    print(input_segments_sorted[n])
    print(segment_dict)

    # Input has been figured out, now we translate to output
    output_dict = {v:k for k, v in segment_dict.items()}
    print(output_dict)

    output_number = ""
    for o in output_segments_sorted[n]:
        output_number = output_number + output_dict[o]

    print(output_segments_sorted[n], output_number, int(output_number))

    sum_val+=int(output_number)

print(sum_val)