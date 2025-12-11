import networkx as nx
import matplotlib.pyplot as plt
from functools import cache


#with open('../data/11_testdata.dat') as f:
with open('../data/11_data.dat') as f:
    lines = [x.strip() for x in f]


# Put the graph in a networkx structure
G = nx.DiGraph()

for line in lines:
    node, cons = line.split(':')
    for con in cons.split():
        G.add_edge(node, con)

#  Part 1 using networkx
#print('Part 1: ', len(list(nx.all_simple_paths(G, 'you', 'out', cutoff=None))))

# we are looking for
# svr -> fft -> dac -> out 

# this does not run in reasonable time
#N_srv_fft =  len(list(nx.all_simple_paths(G, 'svr', 'fft', cutoff=None)))


# Nothing obvious to see on the graph
# nx.draw(G, with_labels=True, node_size=800, 
#         font_size=10, font_weight='bold', arrows=True)
# plt.show()


# Recursive solution using cache
# Just using the networkX G as data structure.
@cache 
def find_N_paths(state, target):
    if state == target:
        return 1
    N_tot=0
    for node in G.successors(state):
        N_tot += find_N_paths(node,target) 
    return N_tot


# Part 1 again for test
print("Part 1: ", find_N_paths('you','out'))

# Part 2
print("Part 2:",  find_N_paths('svr','fft') * find_N_paths('fft','dac') * find_N_paths('dac','out'))
