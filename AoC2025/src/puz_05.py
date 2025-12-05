from copy import deepcopy
from collections import defaultdict #Allows for not checking if a key exists. 
# types =  defaultdict(list) # here we can e.g. append to any key as default will be an empty list

import re


# Multiple groups, returned as a list of lists of strings
#with open('../data/05_testdata.dat') as f:
with open('../data/05_data.dat') as f:
    groups = [group.splitlines() for group in f.read().split('\n\n')]

ingredientIDs = list(map(int,groups[1]))
fressIDranges = [list(map(int, gr.split('-'))) for gr in  groups[0] ]


# part 1, brute force solution
def part1():
    res = 0
    for ID in ingredientIDs:
        for r in fressIDranges:
            if ID in range(r[0],r[1]+1):
                res += 1
                break
    print("Prob 1: ", res)


part1()


#  Part 2, range merge problem

def meargeRanges(fressIDranges):
    meargedRanges = []
    for r in fressIDranges:
        mearged = False
        for mr in meargedRanges:
            if (r[0] in range(mr[0], mr[1]+1)) or (r[1] in range(mr[0], mr[1]+1)):
                mr[1] = max([mr[1], r[1]])
                mr[0] = min([mr[0], r[0]])
                mearged = True
                break
        if not mearged:
            meargedRanges.append(r.copy())
    return meargedRanges


def part2(fressIDranges):
    newIDranges = meargeRanges(fressIDranges)
    while newIDranges != fressIDranges:
        fressIDranges = newIDranges
        newIDranges = meargeRanges(fressIDranges)
        newIDranges = meargeRanges(newIDranges[::-1])  # For fully overlap ranges order  matters
        newIDranges = newIDranges[::-1]

    res = 0
    for r in newIDranges:
        res += r[1]-r[0]+1
    print('Part 2: ', res)


part2(fressIDranges)
