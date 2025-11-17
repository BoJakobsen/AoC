from collections import deque 

# Read maze type data
#with open('../testdata/21_testdata.dat') as f:
with open('../data/21_data.dat') as f:
    map=[x.strip() for x in f]
# map is row, column

# Find start position (marked by an S)
for r, line in enumerate(map):
    if 'S' in line:
        c = line.index('S')
        start = (r, c)

# Size of grid
Nr = len(map)
Nc = len(map[0])

def count_reac(N):
    Parity = N % 2
    visited = set()
    Target = N
    queue = deque()
    queue.append((*start,0))
    reachable = set()
    # Possible move directions
    dirs = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    while queue:
        r,c, N = queue.popleft()
        if N % 2 == Parity:  # is the point reachable taking parity into account
            reachable.add((r,c))
        if N == Target:  # Max number of steps
            continue
        for dir in dirs:
            new_r = r + dir[0]
            new_c = c + dir[1]
            if (map[new_r % Nr][new_c % Nc] == '.' or 
                map[new_r % Nr][new_c % Nc] == 'S') and (new_r,new_c) not in visited:
                visited.add((new_r,new_c))
                queue.append((new_r, new_c, N + 1))

    return (len(reachable))


# Part one (for test)
res = count_reac(64)
print(res)


# Some numbers which are nice to know
Target = 26501365
Nblocks = Target // Nc # 202300
Offset = Target % Nc # 65

# Observation Offset brings us exactly to the edge of the center block, other blocks is
# then just added arround
# in the Manhatten norm we get a nice diamond shape of the reachable points. 
# 

# first interesting configuration is N = Offset + 1 * Nc
#      ^
#     <*>
#      v
#  * is fully covered, <,>,^,V is "V" shaped end caps with 45deg cuts

Nbase = count_reac(Offset + Nc)  # 33108

# second interesting configuration is N = Offset + 2 * Nc
# Telling how much is added

#      ^
#      #
#    <#*#>
#      #
#      v

N45 = count_reac(Offset + Nc * 2) - Nbase  # 58745



N3 = count_reac(Offset + Nc * 3)  # 179936

dN01 = N2 - Nbase
