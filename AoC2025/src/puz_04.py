#from copy import deepcopy
#from collections import defaultdict #Allows for not checking if a key exists. 
# types =  defaultdict(list) # here we can e.g. append to any key as default will be an empty list
#import re


#single block of data
#with open('../data/04_testdata.dat') as f:
with open('../data/04_data.dat') as f:
    map = [x.strip() for x in f]

Nl = len(map)
Nc = len(map[0])

adjs = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]


def part1():
    res = 0
    for l in range(Nl):
        for c in range(Nc):        
            if map[l][c] == '.':
                #print('.', end="")
                continue
            Nrol = 0
            for adj in adjs:
                dl, dc = adj
                test_l, test_c = (l + dl, c + dc)
                if test_l not in range(Nl) or test_c not in range(Nc):
                    continue
                if map[test_l][test_c] == '@':
                    Nrol += 1
            if Nrol < 4:
                #print('#', end="")
                res += 1
            else:
                pass
                #print('@', end="")
        #print('')
    print("Part 1: ", res)

part1()

# #######################
# Part 2
# #######################


def map_to_set(map):
    rolls = set()
    for l in range(Nl):
        for c in range(Nc):
            if map[l][c] == '@':
                rolls.add((l, c))
    return rolls


def find_removable(rolls):
    res = 0
    removable = set()
    for pos in rolls:
        l, c = pos
        Nrol = 0
        for adj in adjs:
            dl, dc = adj
            test_l, test_c = (l + dl, c + dc)
            if test_l not in range(Nl) or test_c not in range(Nc):
                continue
            if (test_l, test_c) in rolls:
                Nrol += 1
            if Nrol >= 4:
                break
        if Nrol < 4:
            removable.add((l, c))
            res += 1
    return res, removable


def part2():
    rolls = map_to_set(map)
    res, removable = find_removable(rolls)
    while len(removable) > 0:
        rolls = rolls - removable
        res_sub, removable = find_removable(rolls)
        res += res_sub
    print("Part 2: ", res)


part2()
