import sys
from functools import cache

sys.setrecursionlimit(1000000000)

with open('../testdata/23_testdata.dat') as f:
#with open('../data/23_data.dat') as f:
    map=[x.strip() for x in f]
# map[row][column]

N_row = len(map)
N_column = len(map[0])

# define start and end
r_start = 0
c_start = 1
start = (r_start, c_start)

r_goal = N_row - 1  # last line
c_goal = N_column - 1 - 1  # second to last column
goal = (r_goal, c_goal)

dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
slopes = ['v', '^', '>', '<']

# Generalized neighbors for both part 1 and part 2
def get_neighbors(row, col, maze = map, part = 'part1'):
    neighbors = []
    if part.lower() == 'part1':
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


# nodes are dict, key: (row, col), value: [connected nodes]
def find_nodes(map = map, part = 'part1'):
    nodes = {}

    # find all nodes
    for r in range(N_row):
        for c in range(N_column):
            if map[r][c] != '#':
                if len(get_neighbors(r, c)) > 2:
                    nodes[(r, c)] = []

    # find connections between nodes, using a simple flood fill.
    for node in nodes:
        queue = [node]
        visited = set()
        while queue:
            cur_node = queue.pop(0)
            visited.add(cur_node)
            if cur_node in nodes and cur_node != node:  # we found a connected node
                nodes[node].append(cur_node)
                continue
            else:
                neighbors = get_neighbors(*cur_node,map, part)
                for neighb in neighbors:
                    if neighb not in visited:
                        queue.append(neighb)
    return nodes

nodes_part1 = find_nodes(map, 'part1')

nodes_part2 = find_nodes(map, 'part2')



# ============================================================================
# Some printing code for debugging
# ============================================================================


# only works if path is returned, as in standard DFS.

# map_with_path = map.copy()
# for step in p:
#     map_with_path[step[0]] = map_with_path[step[0]][:step[1]] + 'o' + map_with_path[step[0]][step[1]+1:]



# for line, orgline in zip(map_with_path,map):
#     print(line,orgline)
