import networkx as nx
import matplotlib.pyplot as plt
from functools import cache


#with open('../data/11_testdata.dat') as f:
with open('../data/11_data.dat') as f:
    lines = [x.strip() for x in f]


# Build directed graph from input
# Format: "node: successor1 successor2 ..."
G = nx.DiGraph()
for line in lines:
    node, cons = line.split(':')
    for con in cons.split():
        G.add_edge(node, con)

# Part 1: Count all paths from 'you' to 'out' using networkx
print('Part 1: ', len(list(nx.all_simple_paths(G, 'you', 'out', cutoff=None))))


## Part 2
# Goal: Count paths through specific sequence: svr -> fft -> dac -> out
# NetworkX's all_simple_paths is too slow for this scale

# Attempted but too slow:
# N_srv_fft =  len(list(nx.all_simple_paths(G, 'svr', 'fft', cutoff=None)))


# Graph visualization (optional, commented out)
# Nothing obvious to see on the graph
# nx.draw(G, with_labels=True, node_size=800, 
#         font_size=10, font_weight='bold', arrows=True)
# plt.show()


# Recursive DFS solution with memoization
# Uses networkx graph as data structure but custom path counting
@cache 
def find_N_paths(state, target):
    """Count number of paths from state to target using DFS with memoization.
    
    Cache key is (state, target) tuple - allows reuse across different targets.
    """
    if state == target:
        return 1  # Base case: reached target

    # Sum paths through all successors
    N_tot=0
    for node in G.successors(state):
        N_tot += find_N_paths(node,target) 
    return N_tot


# Part 1 validation using recursive approach
print("Part 1: ", find_N_paths('you', 'out'))

# Part 2: Multiply paths through each segment of required route
# Total paths = (svr->fft) * (fft->dac) * (dac->out)
print("Part 2:",  find_N_paths('svr', 'fft') *
      find_N_paths('fft', 'dac') * find_N_paths('dac', 'out'))


# Cache performance statistics
stats = find_N_paths.cache_info()
print(f"Cache hits: {stats.hits}")  # 1962
print(f"Cache misses: {stats.misses}")  # 1147
print(f"Hit rate: {stats.hits / (stats.hits + stats.misses) * 100:.1f}%")  # 63.1%



# Alternative: Manual cache implementation (for demonstration)
my_cache = {}


def find_N_paths_mycache(state, target):
    """Same as find_N_paths but with manual dictionary caching.

    """
    if state == target:
        return 1

    if (state, target) in my_cache:
        return my_cache[(state, target)]

    N_tot = 0
    for node in G.successors(state):
        N_tot += find_N_paths_mycache(node, target)
    my_cache[(state, target)] = N_tot
    return N_tot


# Part 1 validation with manual cache
print("Part 1: ", find_N_paths_mycache('you', 'out'))

# Part 2 validation with manual cache
print("Part 2:",  find_N_paths_mycache('svr', 'fft')
      * find_N_paths_mycache('fft', 'dac') * find_N_paths_mycache('dac', 'out'))
