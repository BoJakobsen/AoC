import networkx as nx
from networkx.algorithms import community
#import matplotlib.pyplot as plt

# load lines
#with open('../testdata/25_testdata.dat') as f:
with open('../data/25_data.dat') as f:
   lines = [x.strip() for x in f]

# make dict for diagram  (not really necessary, when using networkx)
diagram = {}
for line in lines:
    splited = line.split(': ')
    diagram[splited[0]] = splited[1].split(' ')


# Build a  graph of all components connections
G = nx.Graph()
for name, connections in diagram.items():
    for out in connections:
        G.add_edge(name, out)


# looking a bit at the graph
# G.number_of_nodes() #1458
# G.number_of_edges() #3266
#
# So a rather large dataset.
# Looks like networkx is the answer most people goes to. 



# ########################
# Solution 1: Girvan-Newman algorithm
# ########################
# Iteratively removes edges with highest betweenness centrality
# to partition graph into communities
#
# suggested by Claude.ai
# https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.community.centrality.girvan_newman.html#networkx.algorithms.community.centrality.girvan_newman

comp = community.girvan_newman(G)

# Find the partition with exactly 2 components
desired_number = 2
# Get partitions at each level
partitions = []
for communities in comp:
    partitions.append(communities)
    if len(communities) == desired_number:
        break


# Verify we removed exactly 3 edges (problem requirement)
edges_removed = len(G.edges()) - sum(len(G.subgraph(c).edges()) 
                                      for c in communities)
print('Edge Removed : ', edges_removed)


# Calculate product of component sizes
res = 1
for com in communities:
   res *= len(com)
print('Product of sizes: ', res)


# ###########################
# Solution 2: minimum_edge_cut
# ###########################
# Directly finds minimum set of edges to disconnect the graph
# More efficient than Girvan-Newman for this specific problem
#
# https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.connectivity.cuts.minimum_edge_cut.html
# hyper-neutrino and Neil Thistlethwaite used this

G.remove_edges_from(nx.minimum_edge_cut(G))
a, b = nx.connected_components(G)
print(len(a) * len(b))



# #######################
# Code for the test input.
# #######################
# Test removing the three edge from the description
#G.remove_edge( 'hfx', 'pzl')
#G.remove_edge( 'bvb', 'cmg')
#G.remove_edge('nvd', 'jqt')

# count size of connected components
#[len(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)]
# works on test data

 
# Draw graph to visualize structure
#nx.draw(G, with_labels=True, node_size=800, \
#         font_size=10, font_weight='bold', arrows=True)
#plt.show()


