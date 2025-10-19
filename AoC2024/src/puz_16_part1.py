import math
with open("../data/16_test.dat") as f:
    ma = [list((x.strip())) for x in f]

nl = len(ma)
nc = len(ma[0])


for l in ma:
    print(*l)


#  Dijkstra's algorithm

dist = {}
orien= {}
prev = {}
Q = {}

# find start point, and populate dictionaries for the algorithm.
for l in range(nl):
    for c in range(nc):
        if ma[l][c] == 'S':
            pos0 = (l,c)
            dist[(l,c)] = 0
            prev[(l,c)] = float('nan')
            Q[(l,c)] = 0
            orien[(l,c)]= (0,1)
        if ma[l][c] == 'E':
            end0 = (l,c)
            prev[(l,c)] = float('nan')
            dist[(l,c)] = float('inf')
            Q[(l,c)] = float("inf")
            orien[(l,c)]= float('nan')
        if ma[l][c] == ".":
            dist[(l,c)] = float('inf')
            prev[(l,c)] = float('nan')
            Q[(l,c)]=float("inf")
            orien[(l,c)]= float('nan')            

dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

while len(Q) > 0:
    u = min(Q, key = Q.get)
    Q.pop(u)
    #if u == end0: break  # for part 2 we want to explore everything
    for dir in dirs:
        v = tupadd(u,dir)
        if v in Q: # still a valid direction
            if orien[u] == dir:  # test if we are continuing same direction 
                alt = dist[u] + 1
            else:
                alt = dist[u] + 1 + 1000
            if alt < dist[v]:
                dist[v] = alt
                Q[v] = alt
                prev[v] = u
                orien[v] = dir

#  Backtrack the solution
S = []
D = []
u = end0
while u == u:  # very strange way to test for nan
    S.append(u)
    D.append(orien[u])
    u = prev[u]

# Calculate answer for part 1 
print(dist[end0])
