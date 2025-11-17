from functools import cache 

# Read maze type data
#with open('../testdata/21_testdata.dat') as f:
with open('../data/21_data.dat') as f:
    map=[x.strip() for x in f]
# map is row, column

# Possible move directions
dirs = [(0, 1), (1, 0), (-1, 0), (0, -1)]

# Find start position (marked by an S)
for r, line in enumerate(map):
    if 'S' in line:
        c = line.index('S')
        start = (r, c)

# Size of grid
Nr = len(map)
Nc = len(map[0])

# function returning the plots accessible
# from pos in N steps
@cache
def find_plots(pos, N):
    plots = set()
    if N == 0:
        plots.add(pos)
        return plots
    for dir in dirs:
        new_pos = (pos[0]+dir[0],  pos[1]+dir[1])
        if 0 <= new_pos[0] <Nr and  0 <= new_pos[1] <Nc and map[new_pos[0]][new_pos[1]] != '#':
            res = find_plots(new_pos, N-1)
            plots = plots.union(res)
    return plots


def part1():
    # Now we just run this and assert the length
    print(len(find_plots(start, 64)))

    # Check stats of the cache
    find_plots.cache_info()
    # for Part 2: CacheInfo(hits=171605, misses=78104, maxsize=None, currsize=78104)

 part1()
