import networkx as nx
import matplotlib.pyplot as plt

#with open('../testdata/20_testdata.dat') as f:
with open('../data/20_data.dat') as f:
   lines = [x.strip() for x in f]
# load as list of lists of integers

module_config_text= [line.split(' -> ') for line in lines]

# unpack the data file, and decode type of module
module_config = {}
for module_text in module_config_text:
    prefix_name, dest_str = module_text
    prefix = prefix_name[0]
    if prefix in '%&':
        name = prefix_name[1:]
        if prefix == '%':
            type = 'FlipFlop'
        else: # &
            type = 'Conjunction'
    else:
        name = prefix_name
        type = ''
    dest = dest_str.split(', ')

    module = {'type': type, 'dest': dest}
    module_config[name] = module

# Configure the module types
for name,module in module_config.items():
    if module['type'] == 'FlipFlop':
        module['state'] = 'off'
    elif module['type'] == 'Conjunction':
        # set up mem, for all inputs to the module
        mem = {}
        for potential_sender, potential_sender_module in module_config.items():
           if name in potential_sender_module['dest']:
               mem[potential_sender] = 'low'
        module['mem'] = mem


def push_signals(module, signal, sender):
    for dest in module['dest']:
        signals.append((dest, signal, sender))


# Processes a signal to a given name 
def process_signal(name,signal, sender):
    if name == 'rx':
        return
    module = module_config[name]
    # Handle the 3 types of modules
    if name == 'broadcaster':
        push_signals(module, signal, name)
    elif module['type'] == 'FlipFlop':
        if signal == 'low': # only do something if the signal is low
            if module['state'] == 'off':
                module['state'] = 'on'
                out_signal = 'high'
            elif module['state'] == 'on':
                module['state'] = 'off'
                out_signal = 'low'
            push_signals(module, out_signal,name)
    elif module['type'] == 'Conjunction':
        module['mem'][sender] = signal
        if set(module['mem'].values()) == set(['high']): # test for all high
            push_signals(module, 'low', name)
        else:
            push_signals(module, 'high', name)




# Part 2
# try some network analysis, as we can't brute force it


#  Network analysis, partly manually, as I need some hint to the structure


# Build a directed graph, of all the modules
G = nx.DiGraph()
for name, module in module_config.items():
   for out in module['dest']:
      G.add_edge(name, out)


# Add colors based on type (thanks claude.ai)
# Create color map based on module type
color_map = []
for node in G.nodes():
    if node == 'broadcaster':
        color_map.append('yellow')
    elif node == 'rx':
        color_map.append('red')
    elif node in module_config:
        if module_config[node]['type'] == 'FlipFlop':
            color_map.append('lightblue')
        elif module_config[node]['type'] == 'Conjunction':
            color_map.append('lightgreen')
        else:
            color_map.append('gray')
    else:
        color_map.append('gray')  # Unknown nodes (like output modules)


# Draw with colors
nx.draw(G, with_labels=True, node_color=color_map, node_size=800, 
        font_size=10, font_weight='bold', arrows=True)
plt.show()


# Based on the plot it is seen that we get an rx out when
# all inputs to df are high
# it is also seen that the 4 input to df are determined by totally separated
# sub-graphs

# Same idea as from the plot, just a bit automated

# look for input to rx
rx_inputs = list(G.predecessors('rx'))
print(f"Modules feeding into rx: {rx_inputs}")
# df Conjunction/memory feed in rx


# look for input to df
df_inputs = list(G.predecessors('df'))
print(f"Modules feeding into df: {df_inputs}")
# ['xl', 'ln', 'xp', 'gp']



# based on above network analysis
# count number of key presses that gives high on the df_inputs
# "hope" that this terminates in reasonable time

# dict for the counts
df_input_cnt = {inp : set() for inp in df_input}


# queue of signals
signals = []

for kk in range(50000): # realisticly high number of iterations
    push_signals(module_config['broadcaster'], 'low', 'button')

    while signals:
        signal = signals.pop(0)
        process_signal(*signal)
        for ind in df_input: # check the input to df
           if module_config['df']['mem'][ind] == 'high':
              df_input_cnt[ind].add(kk+1) #store number of presses (remember +1)


              # look at data
for nam, val in df_input_cnt.items():
   print(nam,sorted(list(val)))
      
# they all follow the pattern
# K0 * N, where K0 is a constant

# find the K0 values
Ks = []
for nam, val in df_input_cnt.items():
   Ks.append(sorted(list(val))[0])


# a solution is the product of the K0's 
# (however can we be sure it is the least??)
res = 1
for k in Ks: 
   res *= k
print(res)
