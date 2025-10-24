from collections import defaultdict
from collections import deque

import matplotlib.pyplot as plt
import numpy as np


#with open('../testdata/18_testdata.dat') as f:
with open('../data/18_data.dat') as f:
    plan=[x.strip().split(' ') for x in f]


# Line, column
dirs = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}


# For plotting the edge
x=[]  # line
y=[]  # column

pos = (0, 0)
visited = set()
visited.add(pos)

# store the visited edge blocks in a dict by line
for dig in plan:
    dir, num, _  = dig
    for k in range(int(num)):
        pos = (pos[0] + dirs[dir][0], pos[1] + dirs[dir][1])
        visited.add(pos)
        x.append(pos[0])
        y.append(pos[1])



# for starters just find one internal point
#plt.plot(x, y,marker='^')
#plt.show()

# A point on the inside, I would like if this was found automatically
#P0 = (50, 100)
P0 = (4,4) # for the test data 


# Simple flood fill
queue = deque()
queue.append(P0)

while queue:
    row, col = queue.popleft()

    for dr,dc in dirs.values():
        neighbor = (row +dr, col + dc)
        if neighbor not in visited:
            visited.add(neighbor)
            queue.append(neighbor) #appends to the right end


print(len(visited))


