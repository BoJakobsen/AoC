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
        signal_count[signal] += 1
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

signals = []
signal_count = {'low': 0, 'high':  0}

def part1():
    # queue of signals
    for k in range(1000):
        signal_count['low'] += 1
        push_signals(module_config['broadcaster'], 'low', 'botton')

        while signals:
            signal = signals.pop(0)
            process_signal(*signal)

    print(signal_count)
    res = signal_count['high']*signal_count['low']
    print(res)


part1()
