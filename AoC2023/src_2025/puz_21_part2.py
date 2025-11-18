from collections import deque
import numpy as np

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

# There is the following type of blocks

# Full block
# Corner block (always 4)
# Edge type 1, 1/8 of a full block
# Edge type 2, 7/8 of a full block


# #### Manual counting on paper :-| and simulating 
#
# Offset + 1 * Nc
# 1 x Full + 4 X Corner
# + 4 X type 1 edge
N1 = count_reac(Offset + Nc)  # 33108
N1a = 0

# Offset + 2 * Nc
# 1 x Full + 4 X Corner
# 4 x full  + 8 X type 1 edge + 4 X type 2 edge 
N2 = count_reac(Offset + Nc * 2)  # 91853
N2a = N2-N1

# Offset + 3 *NC
# 1 x Full + 4 X Corner
# 12 x full  + 12 X type 1 edge + 8 X type 2 edge
N3 = count_reac(Offset + Nc * 3)  # 179936
N3a = N3-N1

# Offset + 4 *NC
# 1 x Full + 4 X Corner
# 24 x full  + 16 X type 1 edge + 12 X type 2 edge
N4 = count_reac(Offset + Nc * 4)  # 297357
N4a = N4-N1

print(f'{N1a=}, {N2a=}, {N3a=}, {N4a=}')

# Look at data,
# x = Nc - 1, y is i the number of the type

# For the full type: (got as a fit)
# 2 * x^2  + 2*x  

# for type 1 edge
# 4 * (x)

# for type 2 edge
# 4 * (x)

# With this definition  of x, edge are now handled as one, which is nice

# Solve two eq with 2 unknowns 
# Ntot - N1 = N_full * a + N_edge * b  # for two of the simulated states
a = np.array([[4, 4], [12, 8 ]])
b = np.array([N2a, N3a,])
x = np.linalg.solve(a, b)

# calculate the total number of full and edges
N_full = 2 * (Nblocks-1) ** 2 + 2 * (Nblocks-1)
N_edge = 4 * (Nblocks-1)

# the total reachable plots are now found as:
res = N_full * x[0] + N_edge * x[1] + N1
print(int(res))

