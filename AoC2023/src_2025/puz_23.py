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


dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
slopes = ['v', '^', '>', '<']
 
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
    """Depth-First Search - finds a path (may not be shortest)"""

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
            if neighbor not in path:
                stack.append((neighbor, path + [neighbor]))  # append to list (at rightmost end)

    return path_lengths


p = dfs(map)

print(max(p)-1)  # path is one longer then number of steps

# map_with_path = map.copy()
# for step in p:
#     map_with_path[step[0]] = map_with_path[step[0]][:step[1]] + 'o' + map_with_path[step[0]][step[1]+1:]



# for line, orgline in zip(map_with_path,map):
#     print(line,orgline)
