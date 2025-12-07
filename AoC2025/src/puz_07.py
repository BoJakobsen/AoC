# Slightly more commented version (some comments by Claude.al)

from collections import deque  # optimized queue
from functools import cache
# single block of data
# with open('../data/07_testdata.dat') as f:
with open('../data/07_data.dat') as f:
    grid = [x.strip() for x in f]

# Grid dimensions
Nl = len(grid)
Nc = len(grid[0])

# Start point, marked by 'S' on line 0
S = (0, grid[0].index('S'))

def part1():
    """BFS to count unique splitters encountered.
    
    Tachyons move downward through the grid. Empty spaces ('.') allow
    continuation, splitters cause branching left and right.
    """
    queue = deque([S])
    splitters_used = set()  # Track unique splitters we've hit
    
    while queue:
        tachyon = queue.popleft()
        new_l, new_c = (tachyon[0] + 1, tachyon[1])  # Move down one row
        
        if new_l == Nl:  # Reached bottom of grid
            continue
        
        if grid[new_l][new_c] == '.':  # Empty space, continue downward
            if (new_l, new_c) not in queue:
                queue.append((new_l, new_c))
            continue
        
        # Must be a splitter - branch left and right
        if (new_l, new_c) not in splitters_used:
            splitters_used.add((new_l, new_c))
            # Add left branch
            if (new_l, new_c-1) not in queue and new_c-1 >= 0:
                queue.append((new_l, new_c-1))
            # Add right branch
            if (new_l, new_c+1) not in queue and new_c+1 < Nc:
                queue.append((new_l, new_c+1))
    
    print('Part 1: ', len(splitters_used))


part1()


# Recursive DFS solution with memoization
@cache  # Memoize based on position - this is the key optimization!
def cnt_worlds(pos):
    """Count number of unique paths (worlds) from this position to grid exit.
    
    Each splitter doubles the number of worlds. The cache decorator prevents
    recalculating paths from positions we've already seen.
    """
    # Exit conditions - fell off an edge
    if pos[0] == Nl or pos[1] < 0 or pos[1] == Nc:
        return 1  # One unique world ending here
    
    if grid[pos[0]][pos[1]] == '.':  # Empty space
        return cnt_worlds((pos[0]+1, pos[1]))  # Continue downward
    
    # Current position is a splitter - split into two worlds
    return cnt_worlds((pos[0], pos[1] + 1)) + cnt_worlds((pos[0], pos[1] - 1))


def part2():
    print('Part 2: ', cnt_worlds(S))


part2()

# Get statistics from cache 
stats = cnt_worlds.cache_info()
print(f"Cache hits: {stats.hits}")
print(f"Cache misses: {stats.misses}")
print(f"Hit rate: {stats.hits / (stats.hits + stats.misses) * 100:.1f}%")


# Simple stack-based DFS solution without memoization
def part2_slow():
    """Explicit path enumeration - explores every path separately.
    
    Works but exponentially slow due to redundant path exploration.
    """
    cnt = 0
    queue = deque([S])  # Using as a stack (pop from end)
    
    while queue:
        tachyon = queue.pop()  # DFS: pop from end
        new_l, new_c = (tachyon[0] + 1, tachyon[1])
        
        if new_l == Nl:  # Reached bottom - one world ends here
            cnt += 1
            continue
        
        if grid[new_l][new_c] == '.':  # Empty space
            if (new_l, new_c) not in queue:
                queue.append((new_l, new_c))
            continue
        
        # Splitter - branch left and right (or count exit if at edge)
        if new_c-1 >= 0:
            queue.append((new_l, new_c-1))
        else:
            cnt += 1  # Left branch exits immediately
        
        if new_c+1 < Nc:
            queue.append((new_l, new_c+1))
        else:
            cnt += 1  # Right branch exits immediately
    
    print(cnt)

# Works on test data, but too slow for full dataset
# part2_slow()
