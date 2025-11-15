# Day 10 Part 2: Count tiles enclosed by pipe loop

# Version with improved comments by Claude.ai

#with open('../testdata/10_2_testdata.dat') as f:
with open('../data/10_data.dat') as f:
    grid = [x.strip() for x in f]

Nrow = len(grid)
Ncol = len(grid[0])

# Find starting position 'S'
for row, line in enumerate(grid):
    if 'S' in line:
        start = (row, line.index('S'))

# Mapping: pipe symbol → which directions it connects
# E.g., 'L' connects North and East
pipes_connecting = {'|': 'NS', '-': 'EW', 'L': 'NE', 'J': 'NW', '7': 'SW',
                    'F': 'SE', 'S': 'NSEW'}

# Direction vectors for moving in grid
dirs = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}

def part1():
    """Trace the pipe loop from start back to start."""
    # Track visited positions (list preserves order for part 2)
    visited_list = []  # Note: set would be faster, but need ordered list later
    visited = set()
    
    cur_pos = start
    
    # Walk the loop until we return to start
    while True:
        visited.add(cur_pos)
        visited_list.append(cur_pos)
        pipe = grid[cur_pos[0]][cur_pos[1]]
        
        # Try each direction this pipe connects
        for dir in pipes_connecting[pipe]:
            test_pos = (cur_pos[0] + dirs[dir][0], cur_pos[1] + dirs[dir][1])
            
            # Check if we've completed the loop (back to start)
            if len(visited) > 2 and test_pos == start:
                break
            
            # Skip if out of bounds
            if test_pos[0] not in range(Nrow) or test_pos[1] not in range(Ncol):
                continue
            
            # Skip if already visited
            if test_pos in visited:
                continue
            
            # Skip empty ground
            test_pipe = grid[test_pos[0]][test_pos[1]]
            if test_pipe == '.':
                continue
            
            # Check if the pipe at test_pos connects back to current position
            connects_back = False
            for test_dir in pipes_connecting[test_pipe]:
                test_back_pos = (test_pos[0] + dirs[test_dir][0],
                                 test_pos[1] + dirs[test_dir][1])
                if test_back_pos == cur_pos:
                    connects_back = True
                    break
            
            # If valid connection found, move to this position
            if connects_back:
                cur_pos = test_pos
                break
        
        # Exit when loop is complete
        if test_pos == start:
            break
    
    # Part 1 answer: max distance is half the loop length
    print(len(visited) / 2)
    return visited, visited_list

# Solve part 1 and get the loop boundary
boundary, boundary_list  = part1()

# ============================================================================
# PART 2 SETUP: Fix the 'S' symbol
# ============================================================================
# 'S' needs to be replaced with the actual pipe type it represents
# Determine this by looking at neighbors in the loop

print(boundary_list[1])   # Next position after start
print(start)         # Start position with 'S'
print(boundary_list[-1])  # Previous position before start

# Example from output:
#   Position (61, 111): pipe '7'
#   Position (62, 111): pipe 'S' (start)
#   Position (62, 110): pipe '-'
#
# Visual layout:
#       7
#      -S
#
# So 'S' connects North and West → must be 'J'

# Manually replace 'S' with correct pipe type
# WARNING: This is specific to this input! Not general solution.
grid[start[0]] = grid[start[0]].replace('S', 'J')


def part2():
    """Count tiles enclosed by the loop using ray casting."""
    ins = set()
    Ninside = 0
    
    # For each position not on the boundary
    for r in range(0, Nrow):
        for c in range(1, Ncol - 1):
            # Skip boundary positions
            if (r, c) in boundary:
                continue
            
            # Ray cast: count boundary crossings to the right
            crossings = 0
            
            # Cast ray from (r, c) horizontally to the right
            for c_test in range(c + 1, Ncol):
                test_point = (r, c_test)
                test_pipe = grid[r][c_test]
                
                # Only count boundary crossings
                if test_point in boundary:
                    # Skip horizontal pipes (don't cross the ray)
                    if test_pipe == '-':
                        continue
                    
                    # If previous position (to the left) is not boundary, count crossing
                    if (test_point[0], test_point[1] - 1) not in boundary:
                        crossings += 1
                        continue
                    
                    # Handle corner cases: trace back along horizontal segment
                    # Find the pipe before the horizontal run
                    n = 1
                    while grid[test_point[0]][test_point[1] - n] == '-':
                        n += 1
                    prew_pipe = grid[test_point[0]][test_point[1] - n]
                    
                    # If segment doesn't form proper horizontal connection, count crossing
                    if (('E' not in pipes_connecting[prew_pipe]) or
                           ('W' not in pipes_connecting[test_pipe])):
                        crossings += 1
                        continue
                    
                    # U-turn pattern: both corners point same direction (North)
                    # Example: L---J (both have 'N', ray crosses boundary)
                    if (('N' in pipes_connecting[prew_pipe]) and
                           ('N' in pipes_connecting[test_pipe])):
                        crossings += 1
                        continue
                    
                    # U-turn pattern: both corners point same direction (South)
                    # Example: F---7 (both have 'S', ray crosses boundary)
                    if (('S' in pipes_connecting[prew_pipe]) and
                           ('S' in pipes_connecting[test_pipe])):
                        crossings += 1
                        continue
                    
                    # Otherwise: S-bend (e.g., F---J or L---7)
                    # Ray enters and exits on same side, doesn't cross
            
            # Odd number of crossings = inside polygon
            if crossings % 2 == 1:
                Ninside += 1
                ins.add((r, c))
    
    print(Ninside)
    return ins

_ = part2()
