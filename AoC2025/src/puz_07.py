from collections import deque  # optimized queue
from functools import cache 

# single block of data
# with open('../data/07_testdata.dat') as f:
with open('../data/07_data.dat') as f:
    grid = [x.strip() for x in f]

# Grid size
Nl = len(grid)
Nc = len(grid[0])

# Start point, marked by 'S' on line 0
S = (0, grid[0].index('S'))  # always start at line 0



def part1():
    queue = deque([S])
    splitters_used = set()

    while queue:
        tachyon = queue.popleft()
        new_l, new_c = (tachyon[0] + 1, tachyon[1])
    #    print(new_l,new_c)
        if new_l == Nl:
            continue  # running out of the end
        if grid[new_l][new_c] == '.':  # a empty space
            if (new_l, new_c) not in queue:
                queue.append((new_l, new_c))
            continue
        if (new_l, new_c) not in splitters_used:  # by filtering, this is a splitter
            splitters_used.add((new_l, new_c))
            if (new_l, new_c-1) not in queue and new_c-1 >= 0:
                queue.append((new_l, new_c-1))
            if (new_l, new_c+1) not in queue and new_c+1 < Nc:
                queue.append((new_l, new_c+1))

    print('Part 1: ', len(splitters_used))


part1()


# Recursive DFS solution, optimized for hash-map
@cache
def cnt_worlds(pos):
    if pos[0] == Nl or pos[1] < 0 or pos[1] == Nc:  # running out of grid
        return 1  # Unique world ending

    if grid[pos[0]][pos[1]] == '.':  # a empty space
        return cnt_worlds((pos[0]+1, pos[1]))  # Progress downwards

    # current pos must be a splitter
    # Split into two worlds
    return cnt_worlds((pos[0], pos[1] + 1)) + cnt_worlds((pos[0], pos[1] - 1))


def part2():
    print('Part 2: ', cnt_worlds(S))


part2()


# Simple stack based DFS solution, no hash-map optimization
def part2_slow():
    cnt = 0
    queue = deque([S])

    while queue:
        tachyon = queue.pop()
        new_l, new_c = (tachyon[0] + 1, tachyon[1])
    #    print(new_l,new_c)
        if new_l == Nl:  # running out of the end, world ending
            cnt += 1
            continue
        if grid[new_l][new_c] == '.':  # a empty space
            if (new_l, new_c) not in queue:
                queue.append((new_l, new_c))
            continue
        # per filtering this is now a splitter
        if new_c-1 >= 0:
            queue.append((new_l, new_c-1))
        else:
            cnt += 1
        if new_c+1 < Nc:
            queue.append((new_l, new_c+1))
        else:
            cnt += 1

    print(cnt)


# Works on test data,  but to slow for the full data set.
# part2_slow()
