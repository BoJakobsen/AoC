import itertools
import numpy as np
import math

with open('../data/8.dat') as f:
    lines=[(x.strip()) for x in f]

# find all antennas and put in dict.
antpos = {}
for ll in range(len(lines)):
    for cc in range(len(lines[ll])):
        char = lines[ll][cc] 
        if char != '.':
            if char in antpos:
                antpos[char].add(((ll,cc)))
            else:
                antpos[char] = set()
                antpos[char].add((ll,cc))


# find set of antinodes
def prob1():
    ants=set()
    for freq in antpos:
        pairs = itertools.combinations(antpos[freq], 2)
        for pair in pairs:
            dx = (pair[0][0]-pair[1][0])
            dy = (pair[0][1]-pair[1][1])
            # handle the two anti notes
            ant1 = (pair[0][0]+dx, pair[0][1]+dy)
            ant2 = (pair[1][0]-dx, pair[1][1]-dy)
            # check for boundary
            if ant1[0] >= 0 and ant1[0] <len(lines) and ant1[1] >= 0 and ant1[1] <len(lines[0]):
                ants.add(ant1)
            if ant2[0] >= 0 and ant2[0] <len(lines) and ant2[1] >= 0 and ant2[1] <len(lines[0]):
                ants.add(ant2)
    return len(ants)

print(prob1())

def prob2():
    ants=set()
    for freq in antpos:
        pairs = itertools.combinations(antpos[freq], 2)
        for pair in pairs:
            dx = (pair[0][0]-pair[1][0])
            dy = (pair[0][1]-pair[1][1])
            scale = math.gcd(dx,dy) 
            #scale with GCD
            dx = dx / scale
            dy = dy / scale
            ant = (pair[0][0], pair[0][1])
            while ant[0] >= 0 and ant[0] <len(lines) and ant[1] >= 0 and ant[1] <len(lines[0]):
                ants.add(ant)
                ant = (ant[0]+dx, ant[1]+dy)
            ant = (pair[0][0], pair[0][1])
            while ant[0] >= 0 and ant[0] <len(lines) and ant[1] >= 0 and ant[1] <len(lines[0]):
                ants.add(ant)
                ant = (ant[0]-dx, ant[1]-dy)
    return (len(ants))

print(prob2())
            


