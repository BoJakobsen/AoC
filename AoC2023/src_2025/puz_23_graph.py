# Day 23: Longest path in hiking trail maze
# Solution uses graph compression to reduce problem size

# Most comments by Claude.ai

#with open('../testdata/23_testdata.dat') as f:
with open('../data/23_data.dat') as f:
    map = [x.strip() for x in f]

# Grid access: map[row][column]
N_row = len(map)
N_column = len(map[0])

# Define start and goal positions
r_start = 0
c_start = 1
start = (r_start, c_start)

r_goal = N_row - 1  # Last row
c_goal = N_column - 1 - 1  # Second to last column (before right wall)
goal = (r_goal, c_goal)

# Movement directions: down, up, right, left
dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

# Slope symbols corresponding to directions
slopes = ['v', '^', '>', '<']

def get_neighbors(row, col, maze=map, part='part1'):
    """
    Get valid neighboring positions from current cell.
    
    Part 1: Respects slopes (forced directions) - creates DAG
    Part 2: Ignores slopes (treats all as '.') - creates undirected graph
    
    Args:
        row, col: Current position
        maze: Grid map
        part: 'part1' or 'part2'
    
    Returns:
        List of (row, col) tuples for valid neighbors
    """
    neighbors = []
    
    # Part 1: If standing on a slope, can only move in that direction
    if part.lower() == 'part1':
        if maze[row][col] in slopes:
            dir = dirs[slopes.index(maze[row][col])]
            new_r = row + dir[0]
            new_c = col + dir[1]
            return [(new_r, new_c)]
    
    # Otherwise (or Part 2), can move in any valid direction
    for dir in dirs:
        new_r = row + dir[0]
        new_c = col + dir[1]
        
        # Check bounds
        if new_c >= 0 and new_c < N_column and new_r >= 0 and new_r < N_row:
            # Skip walls
            if maze[new_r][new_c] == '#':
                continue
            else:
                neighbors.append((new_r, new_c))
    
    return neighbors

def find_nodes(map=map, part='part1'):
    """
    Compress maze into graph of junction nodes.
    
    Junctions are:
    - Start position
    - Goal position  
    - Any position with more than 2 neighbors (branching points)
    
    Returns:
        dict: {node_position: {connected_node: distance, ...}, ...}
        
    Example: nodes[(5,3)] = {(10,3): 8, (5,7): 5}
             means from (5,3) can reach (10,3) in 8 steps
    """
    # Initialize with start and goal as nodes
    nodes = {start: {}, goal: {}}
    
    # Find all junction nodes (degree > 2)
    for r in range(N_row):
        for c in range(N_column):
            if map[r][c] != '#':
                # Junction = more than 2 neighbors (branching point)
                if len(get_neighbors(r, c)) > 2:
                    nodes[(r, c)] = {}
    
    # For each node, find distances to connected nodes using BFS
    for node in nodes:
        queue = [(node, 0)]  # (position, distance_from_node)
        visited = set()
        
        while queue:
            cur_node, cur_distance = queue.pop(0)
            visited.add(cur_node)
            
            # If we reached another junction (not the starting node)
            if cur_node in nodes and cur_node != node:
                # Record the connection and distance
                nodes[node][cur_node] = cur_distance
                continue  # Don't explore past this junction
            else:
                # Continue exploring through corridor
                neighbors = get_neighbors(*cur_node, map, part)
                for neighb in neighbors:
                    if neighb not in visited:
                        queue.append((neighb, cur_distance + 1))
    
    return nodes

# Build compressed graphs for both parts
nodes_part1 = find_nodes(map, 'part1')
nodes_part2 = find_nodes(map, 'part2')

# Note: Graph compression reveals this doesn't create a true DAG for part 1
# (topological sort approach abandoned)
# However, compression reduces ~20,000 cells to ~35 nodes,
# making DFS feasible even though still exponential

def dfs_nodes_longest_track(nodes, current=start, current_path=None):
    """
    Find longest path through compressed graph using DFS.
    
    Args:
        nodes: Compressed graph {node: {neighbor: distance}}
        current: Current node position
        current_path: Tuple of visited nodes (immutable for correct recursion)
    
    Returns:
        Length of longest path from current to goal, or -inf if no path exists
    """
    # Initialize path as empty tuple on first call
    if current_path is None:
        current_path = ()
    
    # Add current node to path (tuple concatenation creates new tuple)
    new_path = current_path + (current,)
    
    # Base case: reached goal
    if current == goal:
        return 0
    
    # Try all connected nodes
    longest = -float('inf')
    for neighbor in nodes[current].keys():
        # Don't revisit nodes (avoid cycles)
        if neighbor not in new_path:
            # Recursively find longest path from neighbor
            N = dfs_nodes_longest_track(nodes, neighbor, new_path)
            
            # If valid path exists, add edge distance
            if N != -float('inf'):
                longest = max(longest, N + nodes[current][neighbor])
    
    return longest

# Solve both parts using compressed graph DFS
print("Part 1:", dfs_nodes_longest_track(nodes_part1))
print("Part 2:", dfs_nodes_longest_track(nodes_part2))  # Still a bit slow (~15s)

