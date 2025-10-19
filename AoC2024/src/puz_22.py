import numpy as np
from collections import defaultdict

with open('../data/22.dat') as f:
    lines = [int((x.strip())) for x in f]



def calcit(num):
    num2 = (num ^ (num * 64)) % 16777216
    num3 = (num2 ^ int(num2 / 32)) % 16777216
    num4 = (num3 ^ num3 * 2048 ) %  16777216
    return num4

# part 1
def part1():
    res = 0
    for num in lines:
        for _ in range(2000):
            num = calcit(num)
        res += num
    print(res)


part1()


def part2():
    # Store all sequences
    price =  [[None]*2001 for _ in range(len(lines))]
    change =  [[None]*2001 for _ in range(len(lines))]
    for idx, num in enumerate(lines):
        price[idx][0] = num % 10
        for kk in range(1,2001):
            num = calcit(num)
            price[idx][kk] = num % 10
            change[idx][kk] = price[idx][kk] - price[idx][kk-1]


    # Store price and 4-sequences
    # A pre-analysis showed this is not to bad, only 40951 unique keys

    keys=defaultdict(list)
    for idx in range(len(lines)):
        cache = set()
        for aa in range(1,2001-4):
            if tuple(change[idx][aa:aa+4]) not in cache:
                keys[tuple(change[idx][aa:aa+4])].append(price[idx][aa+3])
                cache.add(tuple(change[idx][aa:aa+4]))

    # Result can now be found
    res = 0 
    for bb, aa in keys.items():
        if sum(aa) > res :
            res = sum(aa)
    print(res)


part2()
