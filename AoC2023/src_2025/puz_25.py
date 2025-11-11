import networkx as nx
from networkx.algorithms import community
import matplotlib.pyplot as plt

# load lines
#with open('../testdata/25_testdata.dat') as f:
with open('../data/25_data.dat') as f:
   lines = [x.strip() for x in f]

# make dict for diagram 
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


# Try, Girvan-Newman algorithm, as suggested by Claude.ai
comp = community.girvan_newman(G)

desired_number = 2
# Get partitions at each level
partitions = []
for communities in comp:
    partitions.append(communities)
    if len(communities) == desired_number:
        break


# Check how many edges were removed
edges_removed = len(G.edges()) - sum(len(G.subgraph(c).edges()) 
                                      for c in communities)
print('Edge Removed : ', edges_removed)

res = 1
for com in communities:
   res *= len(com)
print('Product of sizes: ', res)




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


