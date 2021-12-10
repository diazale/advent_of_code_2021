"""
Syntax errors: Parse the inputs to see if they are balanced
"""

f = open("../data/input_20211210.txt", "r")
in_data = f.read()
f.close()

chunks = [d for d in in_data.rstrip().split("\n")]

"""
Part 1: 
Stop at the first incorrect closing character on each line
): 3 points.
]: 57 points.
}: 1197 points.
>: 25137 points.
"""

scores = {")":3, "]":57, "}":1197, ">":25137}
closed_dict = {")":"(",
               "]":"[",
               "}":"{",
               ">":"<"}
open_dict = {"(":")",
             "[":"]",
             "{":"}",
             "<":">"}

incorrect = []
incomplete = [] # incomplete chunks (those without errors)

# chunks = [
# "[({(<(())[]>[[{[]{<()<>>",
# "[(()[<>])]({[<{<<[]>>(",
# "{([(<{}[<>[]}>{[]{[(<()>",
# "(((({<>}<{<{<>}{[]{[]{}",
# "[[<[([]))<([[{}[[()]]]",
# "[{[{({}]{}}([{[{{{}}([]",
# "{<[[]]>}<{[{[{[]{()[[[]",
# "[<(<(<(<{}))><([]([]()",
# "<{([([[(<>()){}]>(<<{{",
# "<{([{{}}[<[[[<>{}]]]>[]]"
# ]

# You can open as many brackets as you want, but cannot close them out of order
for chunk in chunks:
    incomplete.append(chunk)
    stack = list()
    for c in chunk:
        if c in closed_dict.values():
            stack.append(c)
        else:
            if stack[-1]==closed_dict[c]:
                stack.pop()
            else:
                incorrect.append(c)
                incomplete.pop() # Remove a chunk if it is incomplete
                break

print("Part 1:", sum([scores[i] for i in incorrect]))

"""
Part 2:
Discard the corrupted lines
Figure out the sequence of closing characters in non-corrupted lines

): 1 point.
]: 2 points.
}: 3 points.
>: 4 points.


"""

scores = {")":1, "]":2, "}":3, ">":4}

def score(chunk_):
    """
    Score is determined by character
    For each character, multiply the total score by 0, then add the value of the character
    :param chunk_: input chunk
    :return: score value
    """
    score_ = 0
    for c_ in chunk_:
        score_ = score_ * 5 + scores[c_]

    return score_

score_list = []

for i in incomplete:
    opening_stack = list()
    closing_stack = list()
    for c in i:
        if c in closed_dict.values():
            # If it's an opening character, add the open bracket to the stack
            # We also require a corresponding closing character
            opening_stack.append(c)
            closing_stack.append(open_dict[c])
        else:
            # If it's a closing character, we can pop the opening stack and closing stack
            # In the end, the closing stack will have the string we need to complete a chunk
            opening_stack.pop()
            closing_stack.pop()

    closing_chunk = "".join(list(reversed(closing_stack)))
    score_list.append(score(closing_chunk))

print(sorted(score_list)[int(len(score_list)/2)])
print(score_list)