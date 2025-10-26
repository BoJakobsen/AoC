# Detailed commented version by claude.ai

import networkx as nx
import matplotlib.pyplot as plt

#with open('../testdata/20_testdata.dat') as f:
with open('../data/20_data.dat') as f:
   lines = [x.strip() for x in f]

# Parse input file into module configuration
module_config_text= [line.split(' -> ') for line in lines]

# Unpack the data file and decode type of module
# Format: %name -> dest1, dest2 (FlipFlop)
#         &name -> dest1, dest2 (Conjunction)
#         broadcaster -> dest1, dest2 (Broadcaster)
module_config = {}
for module_text in module_config_text:
    prefix_name, dest_str = module_text
    prefix = prefix_name[0]
    
    # Decode module type from prefix character
    if prefix in '%&':
        name = prefix_name[1:]  # Remove prefix to get name
        if prefix == '%':
            type = 'FlipFlop'
        else: # &
            type = 'Conjunction'
    else:
        name = prefix_name  # No prefix (broadcaster)
        type = ''
    
    dest = dest_str.split(', ')  # Parse destination list
    
    module = {'type': type, 'dest': dest}
    module_config[name] = module

# Initialize module states
for name, module in module_config.items():
    if module['type'] == 'FlipFlop':
        module['state'] = 'off'  # FlipFlops start in 'off' state
    elif module['type'] == 'Conjunction':
        # Conjunction modules remember last pulse from each input
        # Find all modules that feed into this one
        mem = {}
        for potential_sender, potential_sender_module in module_config.items():
           if name in potential_sender_module['dest']:
               mem[potential_sender] = 'low'  # All inputs start at 'low'
        module['mem'] = mem

def push_signals(module, signal, sender):
    """Add signals to queue for all destinations of this module."""
    for dest in module['dest']:
        signals.append((dest, signal, sender))

def process_signal(name, signal, sender):
    """
    Process a signal sent to a module.
    
    Args:
        name: Module name receiving the signal
        signal: 'low' or 'high' pulse
        sender: Name of module that sent the signal
    """
    # rx is the final output - just return when reached
    if name == 'rx':
        return
    
    module = module_config[name]
    
    # Handle the 3 types of modules
    if name == 'broadcaster':
        # Broadcaster: forward signal to all destinations
        push_signals(module, signal, name)
        
    elif module['type'] == 'FlipFlop':
        # FlipFlop: only responds to low signals, toggles state
        if signal == 'low':
            if module['state'] == 'off':
                module['state'] = 'on'
                out_signal = 'high'
            elif module['state'] == 'on':
                module['state'] = 'off'
                out_signal = 'low'
            push_signals(module, out_signal, name)
            
    elif module['type'] == 'Conjunction':
        # Conjunction: remembers last signal from each input
        # Sends low if ALL inputs are high, otherwise sends high
        module['mem'][sender] = signal
        if set(module['mem'].values()) == set(['high']):  # All inputs high?
            push_signals(module, 'low', name)
        else:
            push_signals(module, 'high', name)

# ============================================================================
# Part 2: Network Analysis Approach
# ============================================================================
# Brute force won't work - answer is in the trillions
# Strategy: Analyze graph structure to find patterns/cycles

# Build a directed graph of all module connections
G = nx.DiGraph()
for name, module in module_config.items():
   for out in module['dest']:
      G.add_edge(name, out)

# Add colors based on module type for visualization (thanks claude.ai)
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

# Draw graph to visualize structure
nx.draw(G, with_labels=True, node_color=color_map, node_size=800, 
        font_size=10, font_weight='bold', arrows=True)
plt.show()

# Based on the plot it is seen that we get an rx output when
# all inputs to df are high
# It is also seen that the 4 inputs to df are determined by totally separated
# sub-graphs (independent binary counters)

# Automated analysis: Find the structure leading to rx
# Look for input to rx
rx_inputs = list(G.predecessors('rx'))
print(f"Modules feeding into rx: {rx_inputs}")
# Result: ['df'] - Single Conjunction module feeds rx

# Look for inputs to df (the gate before rx)
df_inputs = list(G.predecessors('df'))
print(f"Modules feeding into df: {df_inputs}")
# Result: ['xl', 'ln', 'xp', 'gp'] - Four independent Conjunction modules

# Key insight: rx gets low pulse when ALL df inputs are high simultaneously
# Each df input operates independently with its own cycle period
# Answer = LCM of all cycle periods (or product if they're all prime)

# Track when each df input sends a high signal
df_input_cnt = {inp: set() for inp in df_inputs}

# Run simulation to find cycle patterns
signals = []

for kk in range(50000):  # Realistically high number of iterations
    # Press button (sends low pulse to broadcaster)
    push_signals(module_config['broadcaster'], 'low', 'button')
    
    # Process all signals in queue
    while signals:
        signal = signals.pop(0)
        process_signal(*signal)
        
        # Check if any df input has gone high after this button press
        for ind in df_inputs:
           if module_config['df']['mem'][ind] == 'high':
              df_input_cnt[ind].add(kk + 1)  # Store button press number (1-indexed)

# Analyze the patterns
for nam, val in df_input_cnt.items():
   print(nam, sorted(list(val)))

# Observation: Each input follows pattern [K0, 2*K0, 3*K0, ...]
# where K0 is the cycle period for that input

# Extract the cycle period (K0) for each input
Ks = []
for nam, val in df_input_cnt.items():
   Ks.append(sorted(list(val))[0])  # First occurrence = cycle period

print(f"Cycle periods: {Ks}")

# Solution: All inputs must be high simultaneously
# This happens at the product of all periods (assuming coprime periods)
# (For general case, should use LCM, but product works if all are prime)
res = 1
for k in Ks: 
   res *= k

print(f"Part 2: {res}")
