from collections import deque
import numpy as np

# Comments rewritten by Claude.ai
# kept original version in own file, as this
# rewrite is very extensively, and has not been
# totally checked.

# Day 21 Part 2: Garden steps with infinite repeating grid

# Read maze type data
#with open('../testdata/21_testdata.dat') as f:
with open('../data/21_data.dat') as f:
    map = [x.strip() for x in f]

# map is row, column indexed
# Find start position (marked by an S)
for r, line in enumerate(map):
    if 'S' in line:
        c = line.index('S')
        start = (r, c)

# Size of grid (both dimensions are 131 for real input)
Nr = len(map)
Nc = len(map[0])

def count_reac(N):
    """
    Count number of garden plots reachable in exactly N steps.
    Uses BFS with wrapping for infinite grid.
    
    Args:
        N: Number of steps to take
    
    Returns:
        Count of reachable positions with correct parity
    """
    Parity = N % 2  # Target parity (even/odd) for reachable positions
    visited = set()  # Track which (unwrapped) positions we've explored
    Target = N  # Maximum steps allowed
    queue = deque()
    queue.append((*start, 0))  # (row, col, step_count)
    reachable = set()  # Positions reachable with correct parity
    
    # Possible move directions: right, down, up, left
    dirs = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    
    while queue:
        r, c, N = queue.popleft()
        
        # If current position has correct parity, it's reachable
        # (can reach it and have steps left to "waste" returning)
        if N % 2 == Parity:
            reachable.add((r, c))
        
        # Stop exploring from this position if at max steps
        if N == Target:
            continue
        
        # Try all four directions
        for dir in dirs:
            new_r = r + dir[0]
            new_c = c + dir[1]
            
            # Check wrapped position in original grid (infinite repetition)
            # If it's a garden plot and we haven't visited this (unwrapped) position
            if ((map[new_r % Nr][new_c % Nc] == '.' or 
                 map[new_r % Nr][new_c % Nc] == 'S') and 
                (new_r, new_c) not in visited):
                visited.add((new_r, new_c))
                queue.append((new_r, new_c, N + 1))
    
    return len(reachable)

# Part one (for test - 64 steps as per problem)
res = count_reac(64)
print(f"Part 1: {res}")

# ============================================================================
# Part 2: Extrapolate to 26,501,365 steps
# ============================================================================

# Key numbers for the target
Target = 26501365  # Target number of steps (very large!)
Nblocks = Target // Nc  # 202300 - how many grid-widths the diamond extends
Offset = Target % Nc  # 65 - reaches exactly to edge of center grid

# KEY OBSERVATION: 
# Offset (65) brings us exactly to the edge of the center block.
# Additional blocks form a diamond pattern in Manhattan distance.
# 
# After Offset + k*Nc steps, we have a diamond k grids wide.
# The diamond contains different types of grid copies:
#
#   1. Center + 4 corners: Always same configuration (N1 term)
#   2. Fully filled grids: Increase as k^2 
#   3. Edge grids: Partially filled, increase linearly with k
#
# Strategy: 
#   - Simulate for small values of k (1, 2, 3, 4)
#   - Extract pattern for full grids and edge grids
#   - Extrapolate to k = 202300

# Run simulations for small diamond sizes
# Pattern: Offset + k * Nc steps creates diamond k grids wide

# k=1: One grid-width diamond
# Contains: 1 center full + 4 corners + 4 small edge pieces (type 1)
N1 = count_reac(Offset + Nc)  # 33108
N1a = 0  # Baseline (contains center + corners only)

# k=2: Two grid-widths diamond  
# Adds: 4 full grids + 4 more type 1 edges + 4 type 2 edges
N2 = count_reac(Offset + Nc * 2)  # 91853
N2a = N2 - N1  # Additional reachable plots beyond baseline

# k=3: Three grid-widths diamond
# Adds: 8 more full grids + 4 more type 1 edges + 4 more type 2 edges  
N3 = count_reac(Offset + Nc * 3)  # 179936
N3a = N3 - N1  # Additional beyond baseline

# k=4: Four grid-widths diamond (for verification)
# Adds: 12 more full grids + 4 more type 1 edges + 4 more type 2 edges
N4 = count_reac(Offset + Nc * 4)  # 297357
N4a = N4 - N1  # Additional beyond baseline

print(f'{N1a=}, {N2a=}, {N3a=}, {N4a=}')

# ============================================================================
# Pattern Analysis (from manual counting on paper!)
# ============================================================================
#
# For diamond k grids wide (k = Nblocks - 1 for our case):
#
# Full grids:  2*k^2 + 2*k  (forms the bulk of the diamond)
# Type 1 edge: 4*k           (small edge pieces)
# Type 2 edge: 4*k           (large edge pieces)
#
# Since type 1 and 2 both scale as 4*k, we can combine them!
# Total edge contribution: 4*k * (average plots per edge)

# Set up system of equations to find contribution per full grid and per edge
# For k=2: N2a = (full_count_at_k2) * x[0] + (edge_count_at_k2) * x[1]
# For k=3: N3a = (full_count_at_k3) * x[0] + (edge_count_at_k3) * x[1]
#
# Where x[0] = plots per full grid, x[1] = plots per edge grid (averaged)

a = np.array([[4, 4],   # k=2: 4 full grids, 4 edge grids (type1+type2 combined)
              [12, 8]])  # k=3: 12 full grids, 8 edge grids
b = np.array([N2a, N3a])

# Solve for x[0] (full grid contribution) and x[1] (edge contribution)
x = np.linalg.solve(a, b)

print(f"Plots per full grid: {x[0]:.1f}")
print(f"Plots per edge (avg): {x[1]:.1f}")

# Calculate counts for target diamond size (k = Nblocks - 1 = 202299)
N_full = 2 * (Nblocks - 1) ** 2 + 2 * (Nblocks - 1)  # Total full grids
N_edge = 4 * (Nblocks - 1)  # Total edge grids

# Final answer: baseline (N1) + full grids contribution + edge contribution
res = N_full * x[0] + N_edge * x[1] + N1

print(f"Part 2: {int(res)}")
