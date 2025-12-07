import math

# single block of data
# with open('../data/06_testdata.dat') as f:
with open('../data/06_data.dat') as f:
    lines = [x for x in f]


def prob1():
    """Process data horizontally: each row contains numbers followed by an operator."""
    dat = [l.strip().split() for l in lines]
    problems = list(zip(*dat))  # Transpose: columns become rows
    res = 0

    for problem in problems:
        # Last element is the operator, rest are numbers
        if problem[-1] == '*':
            res += (math.prod(map(int, problem[:-1])))
        else:  # Assume '+'
            res += (sum(map(int, problem[:-1]))) 

    print('Prob 1; ', res)


prob1()


def prob2():
    """Process data vertically: read numbers column-wise, operators in last row."""
    res = 0
    op = lines[-1].split()  # Operators from last line
    kk = 0  # Operator index
    numbs = []  # Accumulate numbers for current operation

    # Process each column position
    for c in range(len(lines[0])):
        string = ''
        # Build vertical string from all rows except last (operators row)
        for l in range(len(lines) - 1):
            string += lines[l][c]

        if any(char.isdigit() for char in string):  # Column contains part of a number
            numbs.append(int(string))
        else:  # Hit a separator (spaces) - apply operation
            if op[kk] == '*':
                res += math.prod(numbs)
            else:
                res += sum(numbs)
            kk += 1  # Move to next operator
            numbs = []  # Reset for next group

    print('Prob 2: ', res)


prob2()
