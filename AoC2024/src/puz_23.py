from functools import cache 
from collections import defaultdict
import networkx as nx
import copy
with open('../data/23.dat') as f:
    lines = [(x.strip()) for x in f]

# Make a map of the lan
lan = defaultdict(list)
for line in lines:
    a ,b = line.split('-')
    lan[a].append(b)
    lan[b].append(a)

sets = []
def find_leafs(nodes, level):
    global sets
    if level == 3:
        if nodes[level]  ==  nodes[0]:
            if set(nodes[0:3]) not in sets:
                sets.append(set(nodes[0:3]))
        return
    for n in lan[nodes[level]]:
        if level < 2 and n == nodes[0] : continue # skip back links 
        nodes.append(n)
        find_leafs(nodes,level +1)
        nodes.pop()
    return

def part1():
    for name in lan.keys():
        if name[0] == 't':
            nodes = [name]
            find_leafs(nodes,0)
    print(len(sets))

part1()

# Part 2
# This is an example of finding all maximal cliques in an undirected graph    
# Bron–Kerbosch algorithm is an enumeration algorithm for this
# https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm

sets = []
def BronKerbosch1(R, P, X):
    global sets
    if len(P) == 0 and len(X) == 0 :
        if R not in sets:
            sets.append(R)
#        print(R)
    for v in P:
        P2 = copy.copy(P)
        N = set(lan[v])
        BronKerbosch1(R.union(set([v])), P2.intersection(N), X.intersection(N))
        P2.remove(v)
        X.add(v)

p = set(lan.keys())
r = set()
x = set()
#BronKerbosch1(r,p,x)
# THIS is too slow it seems,



# An nice library also exists,
# and https://networkx.org which can do it directly.

G = nx.Graph()
for line in lines:
    a ,b = line.split('-')
    G.add_edge(a,b)

print(','.join(sorted(max(nx.find_cliques(G), key=len))))
# Work, but maybe not the most fun solution.


## Inspiret by Hyperneutrinos youtube solution
#  Second try on a recursive solution

# Make a map of the lan, this time a set to avoided converting back an forward to sets 
lan = defaultdict(set)
for line in lines:
    a ,b = line.split('-')
    lan[a].add(b)
    lan[b].add(a)

    
# global set of Cliques to be populated and used in the recursion 
cliques = set()

def find_cliques(node,cliq):
    c = tuple(sorted(cliq))  # Ordered tuple of current cliq
    if c in cliques: return  # if this is one we already have seen, return
    cliques.add(tuple(sorted(cliq)))  # else add to total list and process children
    for child in lan[node]:
        if child in cliq: continue # This node is already in the cliq set
        if all([c in lan[child] for c in cliq]): # child is connected to all in cliq
            find_cliques(child, {*cliq, child})


# Now loop all nodes and find all cliques
for node in lan.keys():
    find_cliques(node,{node})
# Works but is much slower than the NetworkX lib function (nu surprise)

# find the longest tuple, (max using len as "key"), is already sorted
print(','.join(max(cliques, key = len)))

