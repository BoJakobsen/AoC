# Some usefully stuff for working with AoC problems
# Potentially nice to  just run before solving

# Libraries very often used (should properly just be loaded always)
import numpy as np
import re
import copy

from collections import defaultdict
from collections import deque

#from functools import cache 
# add @cache before eg recursive functions, very efficient. 

#import itertools # # for e.g. permutations

#import networkx as nx # for graphs, is a large library

# import heapq  # for priority queue in e.g.  Dijkstra's algorithm


    
##  Some functions 

# Basic loader
def baseloader(filename):
    with open(filename) as f:
        lines = [(x.strip()) for x in f]
    return lines

# Nice for working with tuples representing coordinates
def tupadd(a, b):
    res = tuple(map(lambda i, j: i + j, a, b))
    return res


# map is given as list of strings (or lists)
# coordinate as tuple
def checkbound(lines, coord):
    res = coord[0] >= 0 and coord[0] < len(lines) and coord[1] >= 0 and coord[1] < len(lines[0])
    return res


# Mapping a map to a dict with coordinates of the points
# basechar is the one "not to map" (empty points in map)
def maptodict(lines, basechar):
    pos = {}
    for ll in range(len(lines)):
        for cc in range(len(lines[ll])):
            char = lines[ll][cc]
            if char not in basechar:
                if char in pos:
                    pos[char].add(((ll, cc)))
                else:
                    pos[char] = set()
                    pos[char].add((ll, cc))
    return pos


## Some snippets that can maybe be usefull


## Some loader snippets

# lines in a list
# with open(filename) as f:
#     lines = [(x.strip()) for x in f]


# Flexible e.g. for parts separated with blank line
# with open('data/24_test.dat') as f:
#     a = f.read().strip()
# lines, gates = a.split('\n\n')
# for line in lines.split('\n'):
#     a,b = line.split(': ')


# break at a empty line, for two parts
# for line in file:
#    if line.isspace(): break
#    rules.append(list(map(int, line.split("|"))))


# For finding number I guess (from Hyperneutrino)
#for line in open(0):
#    robots.append(tuple(map(int, re.findall(r"-?\d+", line))))


## Graph stuff

# Find the maximal clique in a graph, from day 23,  
# G = nx.Graph()
# for line in lines:
#    a ,b = line.split('-')
#    G.add_edge(a,b)
# ','.join(sorted(max(nx.find_cliques(G), key=len)))


## Slicing    

# Horizontal slicing is easy
# map[2][3:]

# Vertically slicing
# "".join([a[2] for a in map[3:]  ])
# is a bit not so nice

# Numpy arrays are much easier to slice.
# a= np.array(map)
# b = a[:,1]  # by reference ! so we can just assign
# ind=np.where(b=='O')
# b[ind] = 'X'


## Links to other AoC resources

# Nice list of python snippets from AoC
# https://www.reddit.com/r/adventofcode/comments/1gsl4fm/share_your_favorite_tricks_and_snippets/

# Nice post, will all old AoC problems
# https://www.reddit.com/r/adventofcode/comments/1gdw4cj/450_stars_a_categorization_and_megaguide/


# Hyperneutrino, vvery nice solutions in Python and god youtube videos
# https://github.com/hyperneutrino/advent-of-code/


