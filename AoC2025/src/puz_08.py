import networkx as nx

#with open('../data/08_testdata.dat') as f:
with open('../data/08_data.dat') as f:
    coords = [list(map(int,x.strip().split(','))) for x in f]


def calc_dist(a, b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2 

# Calculate distances between all pairs (skipping the sqrt for speed)
dists = []
for kk in range(len(coords)):
    for ll in range(kk+1,len(coords)):
        dists.append([calc_dist(coords[kk], coords[ll]), kk, ll])

dists.sort() # sort distances


def part1():
    G = nx.Graph() 
    Nconnetions = 1000 # 10 for test data, 1000 for real data
    for kk in range(Nconnetions):
        G.add_edge(dists[kk][1], dists[kk][2])

    length_of_subnets = [len(c) for c in sorted(nx.connected_components(G),
                                                key=len, reverse=True)]
    res = 1
    for kk in range(3):
        res *= length_of_subnets[kk]
    print('Part 1: ', res)


part1()


def part2():
    G = nx.Graph()
    G.add_nodes_from(range(len(coords)))  # add all nodes

    kk = -1
    # Add connections untall all are connected
    while nx.number_connected_components(G) > 1: 
        kk += 1
        G.add_edge(dists[kk][1], dists[kk][2])

    print('Part 2:', coords[dists[kk][1]][0] * coords[dists[kk][2]][0])


part2()

