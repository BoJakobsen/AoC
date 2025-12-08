import networkx as nx

# Some comments are by Claude.ai

#with open('../data/08_testdata.dat') as f:
with open('../data/08_data.dat') as f:
    coords = [list(map(int,x.strip().split(','))) for x in f]


def calc_dist(a, b):
    """Calculate squared Euclidean distance in 3D space.

    Skips sqrt for performance - ordering is preserved.
    """
    return (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2


# Calculate distances between all pairs of coordinates
# Store as [distance, index_a, index_b]
dists = []
for kk in range(len(coords)):
    for ll in range(kk+1, len(coords)):  # Only upper triangle (avoid duplicates)
        dists.append([calc_dist(coords[kk], coords[ll]), kk, ll])

dists.sort()  # Sort by distance (closest pairs first)


def part1():
    """Find product of sizes of three largest connected components.

    Build graph using N closest connections, then find largest subnets.
    """
    G = nx.Graph()
    Nconnetions = 1000  # 10 for test data, 1000 for real data

    # Add the N closest connections
    for kk in range(Nconnetions):
        G.add_edge(dists[kk][1], dists[kk][2])

    # Find sizes of all connected components, sorted largest first
    length_of_subnets = [len(c) for c in sorted(nx.connected_components(G),
                                                key=len, reverse=True)]

    # Multiply sizes of three largest subnets
    res = 1
    for kk in range(3):
        res *= length_of_subnets[kk]

    print('Part 1: ', res)


part1()


def part2():
    """Find the connection that finally unifies all components.

    Add edges by increasing distance until graph becomes fully connected.
    """
    G = nx.Graph()
    G.add_nodes_from(range(len(coords)))  # Start with all isolated nodes

    kk = -1
    # Add connections in order of distance until only 1 component remains
    while nx.number_connected_components(G) > 1:
        kk += 1
        G.add_edge(dists[kk][1], dists[kk][2])

    # The kk-th edge was the one that connected everything
    # Return product of x-coordinates of the two connected points
    print('Part 2:', coords[dists[kk][1]][0] * coords[dists[kk][2]][0])


part2()
