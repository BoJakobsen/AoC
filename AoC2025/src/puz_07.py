# from copy import deepcopy
# from collections import defaultdict #Allows for not checking if a key exists. 
# # types =  defaultdict(list) # here we can e.g. append to any key as default will be an empty list

# import re
# import math

from collections import deque  # optimized queue

#single block of data
#with open('../data/07_testdata.dat') as f:
with open('../data/07_data.dat') as f:
    grid = [x.strip() for x in f]

Nl = len(grid)
Nc = len(grid[0])

S = (0, grid[0].index('S'))  # always start at line 0
queue = deque([S])
splitters_used = set()

while queue:
    tachyon  = queue.popleft()
    new_l, new_c = (tachyon[0] + 1, tachyon[1])
#    print(new_l,new_c)
    if new_l == Nl : continue # running out of the end
    if grid[new_l][new_c] == '.':  # a empty space
        if (new_l,new_c) not in queue: 
            queue.append((new_l,new_c))
        continue
    if  (new_l, new_c) not in splitters_used: # by filtering, this is a splitter
        splitters_used.add((new_l,new_c))
        if (new_l,new_c-1) not in queue and new_c-1 >= 0: 
            queue.append((new_l,new_c-1))
        if (new_l,new_c+1) not in queue and new_c+1 < Nc:  
            queue.append((new_l,new_c+1))

print(len(splitters_used))
        

