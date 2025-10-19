import math
import heapq
from collections import defaultdict

with open("../data/16.dat") as f:
    ma = [list((x.strip())) for x in f]

nl = len(ma)
nc = len(ma[0])


# # Find start point, and populate dictionaries for the algorithm.
for l in range(nl):
     for c in range(nc):
         if ma[l][c] == 'S':
             pos0 = (l,c)
         if ma[l][c] == 'E':
             end0 = (l,c)

# Print Maze
# for l in ma:
#     print(*l)


#  Dijkstra's algorithm (inspired by Hyper Neutrino's implementation, much simpler)
#  Using abstract nodes of position and orientation.


# Calculate answer for part 1

# priority queue
Q = []
# dist, l, c, dl, dc 
heapq.heappush(Q, (0, *pos0,0,1))

# Set for processed (not visited) notes
processed = {(0, *pos0, 0, 1)}

while Q:
    u = heapq.heappop(Q)
    dist, l, c, dl, dc = u
    processed.add((l, c, dl, dc))
    if (l, c) == end0:
        res = dist
        break  # 
    for child in [(dist +1, l+dl, c+dc, dl, dc), (dist + 1000, l, c, dc, -dl), (dist + 1000, l, c, -dc, dl)]:
        ndist, nl, nc, ndl, dnc = child
        if ma[nl][nc] == '#' : continue
        if (nl, nc, ndl, dnc) in processed: continue 
        heapq.heappush(Q,(ndist,nl, nc, ndl, dnc))

print(dist) # works


# Part 2
# Modified Dijkstra's algorithm, tracing all routes and storing parents
# Notice, this is not an "optimal" implementation, see Hyper Neutrino for some tricks.


# priority queue
Q = []
# dist, l, c, dl, dc 
heapq.heappush(Q, (0, *pos0,0,1))

# Set for processed (not visited) notes
processed = {(0, *pos0, 0, 1)}
prev = defaultdict(set)
prev[(*pos0, 0, 1)] = [(None, None, None, None, None)]
minval = float('inf')

while Q:
    u = heapq.heappop(Q)
    dist, l, c, dl, dc = u
    processed.add((l, c, dl, dc))
    if (l, c) == end0: # We do not stop  
        if dist < minval: # Keep track of shortest path
            minval = dist
    for child in [(dist +1, l+dl, c+dc, dl, dc), (dist + 1000, l, c, dc, -dl), (dist + 1000, l, c, -dc, dl)]:
        ndist, nl, nc, ndl, ndc = child
        if ma[nl][nc] == '#' : continue
        if (nl, nc, ndl, ndc) in processed: continue
        prev[(nl, nc, ndl, ndc)].add((dist, l, c, dl, dc))
        heapq.heappush(Q,(ndist,nl, nc, ndl, ndc))

print(minval)

# Best paths can now be found by backtracking on all paths that
# ends up with minval in total

seen = set()  # Set of all points touched by a "best path"
def backtrace(node, cost):
    l, c, dl, dc = node
    seen.add((l ,c))
    if (l, c) == pos0:
        return
    for parent in prev[node] :
        pcost , pl, pc, pdl, pdc = parent # pcost is price to get to parent
        # If we are on a "best path" cost difference should be either 1 or 1000
        if (l, c) == (pl, pc) and cost == pcost + 1000:  # parent -> node was rotation
            backtrace((pl, pc, pdl, pdc), pcost)
        if (l, c) != (pl, pc) and cost == pcost +1: # parent -> node was step
            backtrace((pl, pc, pdl, pdc), pcost)
    return

# For test look at all endings
# for node in prev.keys():
#     l, c, dl, dc = node
#     if (l,c) == end0:
#         print(node, prev[node])

# We need to test all 4 end nodes (one pos, 4 for directions)
for endnode in [(*end0, -1, 0), (*end0, 1, 0), (*end0, 0, -1), (*end0, 0, 1)]:
    backtrace(endnode, minval)
res = len(seen)
print(res)
