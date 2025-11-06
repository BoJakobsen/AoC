import sys
from functools import cache

sys.setrecursionlimit(1000000000)

#with open('../testdata/23_testdata.dat') as f:
with open('../data/23_data.dat') as f:
    map=[x.strip() for x in f]
# map[row][column]

N_row = len(map)
N_column = len(map[0])

# define start and end
l_start = 0
c_start = 1

l_goal = N_row - 1  # last line
c_goal = N_column - 1 - 1  # second to last column
goal = (l_goal, c_goal)

dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
slopes = ['v', '^', '>', '<']

# ============================================================================
# Part 1: 
# ============================================================================

def get_neighbors(maze, row, col):
    neighbors = []
    if maze[row][col] in slopes:  # we are on a slope
        dir = dirs[slopes.index(maze[row][col])]
        new_r = row + dir[0]
        new_c = col + dir[1]
        return [(new_r, new_c)]
    for dir in dirs:
        new_r = row + dir[0]
        new_c = col + dir[1]
        if new_c >= 0 and new_c < N_column and new_r >= 0 and new_r < N_row:
            if maze[new_r][new_c] == '#':
                continue
            else:
                neighbors.append((new_r, new_c))
    return neighbors


def dfs(maze):
    """Modified Depth-First Search, finds all paths.
       Returns only the length of these paths. 
    """

    path_lengths = []
    start = (l_start, c_start)

    # Stack stores (current_position, path)
    stack = [(start, [start])]
#    visited = set()

    while stack:
        (row, col), path = stack.pop()  # last item of list (Rightmost)

#        if (row, col) in visited:
#            continue

#        visited.add((row, col))

        if (row, col) == (l_goal, c_goal):
            path_lengths.append(len(path))

        for neighbor in get_neighbors(maze, row, col):
            if neighbor not in path:  # test if the point has been visited on this path
                stack.append((neighbor, path + [neighbor]))  # append to list (at rightmost end)

    return path_lengths

def part1():
    p = dfs(map)
    print(max(p)-1)  # path is one step longer then number of steps
#part1()

# ============================================================================
# Part 2: Simple implementation based on part 1, way to slow, but works on test data
# ============================================================================

def get_neighbors2(maze, row, col):
    neighbors = []
    for dir in dirs:
        new_r = row + dir[0]
        new_c = col + dir[1]
        if new_c >= 0 and new_c < N_column and new_r >= 0 and new_r < N_row:
            if maze[new_r][new_c] == '#':
                continue
            else:
                neighbors.append((new_r, new_c))
    return neighbors


def dfs2(maze):
    """Modified Depth-First Search, finds all paths.
       Returns only the length of these paths. 
    """

    path_lengths = []
    start = (l_start, c_start)

    # Stack stores (current_position, path)
    stack = [(start, [start])]

    while stack:
        (row, col), path = stack.pop()  # last item of list (Rightmost)

        if (row, col) == (l_goal, c_goal):
            path_lengths.append(len(path))

        for neighbor in get_neighbors2(maze, row, col):
            if neighbor not in path:  # test if the point has been visited on this path
                stack.append((neighbor, path + [neighbor]))  # append to list (at rightmost end)

    return path_lengths


#p = dfs2(map)
#print(max(p)-1)  # path is one step longer then number of steps


# ============================================================================
# Part 2: Recursive, based on good old stackoverflow
# ============================================================================
path_lengths = []


def dfs_recursive_all_traces(maze, current, end, path):
    path_so_far = path.copy()
    # add current note to the path
    path_so_far.append(current)
    for neighbor in get_neighbors2(maze, *current):
        if neighbor == end:
            path_lengths.append(len(path_so_far)) 
            print("found")
        else:
            if neighbor not in path_so_far:  # Check that we are not going back to visited node
                dfs_recursive_all_traces(maze, neighbor, end, path_so_far)


#p = dfs_recursive_all_traces(map, (l_start, c_start), (l_goal, c_goal), [])

# will work but is way to slow still. 


# ============================================================================
# Part 2: Recursive, only looking for path length, inspiration from Claude.io
# ============================================================================
@cache
def dfs_longest_track(current=(l_start, c_start), current_path=None):

    if current_path is None:
        current_path = ()

    new_path = current_path + (current,) # nice way to append to tuple
    if current == goal:
        return 0

    longest = -float('inf')
    for neighbor in get_neighbors2(map, *current):
        if neighbor not in new_path:  # Check that we are not going back to visited node
            N = dfs_longest_track(neighbor, new_path)
            if N != -float('inf'):
                longest = max(longest, N+1)
    return longest
            
dfs_longest_track()

# Still breaks on a recursion depth error




# ============================================================================
# Some printing code for debugging
# ============================================================================


# only works if path is returned, as in standard DFS.

# map_with_path = map.copy()
# for step in p:
#     map_with_path[step[0]] = map_with_path[step[0]][:step[1]] + 'o' + map_with_path[step[0]][step[1]+1:]



# for line, orgline in zip(map_with_path,map):
#     print(line,orgline)
