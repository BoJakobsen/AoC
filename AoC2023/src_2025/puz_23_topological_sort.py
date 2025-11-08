#with open('../testdata/23_testdata.dat') as f:
with open('../data/23_data.dat') as f:
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
    nodes = {start : {}, goal : {}}

    # find all nodes
    for r in range(N_row):
        for c in range(N_column):
            if map[r][c] != '#':
                if len(get_neighbors(r, c)) > 2:
                    nodes[(r, c)] = {}

    # find connections between nodes, using a simple flood fill.
    for node in nodes:
        queue = [(node,0)]
        visited = set()
        while queue:
            cur_node, cur_distance  = queue.pop(0)
            visited.add(cur_node)
            if cur_node in nodes and cur_node != node:  # we found a connected node
                nodes[node][cur_node] = cur_distance
                continue
            else:
                neighbors = get_neighbors(*cur_node,map, part)
                for neighb in neighbors:
                    if neighb not in visited:
                        queue.append((neighb,cur_distance + 1))
    return nodes

nodes_part1 = find_nodes(map, 'part1')

nodes_part2 = find_nodes(map, 'part2')


# Realize that this does not build a DAG and hence topological sorting does not work
# properly for part 1 but that is not the hard part
# Back to drawing board

# However as we now have compressed the maze to a graph with rather small
# number of notes, it should be possible to sole using a simple DFS search.

# reuse count path length from puz_23.py
def dfs_nodes_longest_track(nodes, current=start, current_path=None):
    if current_path is None:
        current_path = ()

    new_path = current_path + (current,) # nice way to append to tuple
    if current == goal:
        return 0

    longest = -float('inf')
    for neighbor in nodes[current].keys():
        if neighbor not in new_path:  # Check that we are not going back to visited node
            N = dfs_nodes_longest_track(nodes, neighbor, new_path)
            if N != -float('inf'):
                longest = max(longest, N+nodes[current][neighbor])
    return longest



# Part 1 and two can now be solved
dfs_nodes_longest_track(nodes_part1)
dfs_nodes_longest_track(nodes_part2) # still a bit slow



# ============================================================================
# Some printing code for debugging
# ============================================================================


# only works if path is returned, as in standard DFS.

# map_with_path = map.copy()
# for step in p:
#     map_with_path[step[0]] = map_with_path[step[0]][:step[1]] + 'o' + map_with_path[step[0]][step[1]+1:]



# for line, orgline in zip(map_with_path,map):
#     print(line,orgline)
