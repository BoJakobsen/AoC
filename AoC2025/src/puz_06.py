import math

# single block of data
#with open('../data/06_testdata.dat') as f:
with open('../data/06_data.dat') as f:
    lines = [x for x in f]


def prob1():
    dat = [l.strip().split() for l in lines]
    problems = list(zip(*dat))
    res = 0
    for problem in problems:
        if problem[-1] == '*':
            res += (math.prod(map(int, problem[:-1])))
        else:
            res += (sum(map(int, problem[:-1]))) 

    print('Prob 1; ', res)


prob1()


def prob2():
    res = 0
    op = lines[-1].split()
    kk = 0
    numbs = []
    for c in range(len(lines[0])):
        string = ''
        for l in range(len(lines) - 1):
            string += lines[l][c]
        if any(char.isdigit() for char in string): # have number
            numbs.append(int(string))
        else:
            if op[kk] == '*':
                res += math.prod(numbs)
            else:
                res += sum(numbs)
            kk += 1
            numbs = []
    print('Prob 2: ', res)


prob2()
