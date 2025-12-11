from z3 import Optimize, Int, Solver
from functools import cache
from collections import deque 

#with open('../data/10_testdata.dat') as f:
with open('../data/10_data.dat') as f:
    lines = [x.strip().split() for x in f]


def sw_to_num(sw):
    """Convert list of bit positions to bitmask.
    
    Example: [0, 2, 3] -> 2^0 + 2^2 + 2^3 = 13 (binary: 1101)
    This bitmask can be XORed with a state to toggle those bits.
    """
    num = 0
    for bit in sw:
        num += 2**bit
    return num

def part1():
    """Find minimum button presses to reach target patterns using BFS.
    
    Each button toggles specific bits (XOR operation).
    Start from state 0 (all bits off), find shortest path to target.
    """
    # Parse input into binary representations
    targets = []
    switches = []
    
    for line in lines:
        # Convert pattern like ".#.##" to binary number
        # '.' = 0, '#' = 1, reversed because bit 0 is rightmost
        # Example: ".#.##" -> "##.#." -> "11010" -> 26
        targets.append(int(line[0][1:-1].replace('.','0').replace('#','1')[::-1], 2))
        
        # Convert button effects to bitmasks
        # Each button has positions like "(0,2,3)"
        sws = [sw[1:-1].split(',') for sw in line[1:-1]]
        switches.append([sw_to_num(list(map(int, sw))) for sw in sws])
    
    res = 0
  
    
    # Solve each machine independently
    for target, switch in zip(targets, switches):
        queue = deque()
        queue.append([0, 0])  # [current_state, num_presses]
        visited = set() # Forgot this in original solution, thanks Claude.ai

        # BFS: explore states by increasing number of presses
        while queue:
            state, N = queue.popleft()
            
            if state == target:
                res += N  # Found shortest path
                break
            
            # Try pressing each button
            for sw in switch:
                new_state = state ^ sw 
                if  new_state not in visited:
                    queue.append([new_state, N + 1])  # XOR toggles bits
                    visited.add(new_state)
    
    print("Part 1: ", res)

# part 1 is a bit slow, but reasonable
part1()


# Part 2: Minimize total button presses to reach all targets
def part2():
    """
    For each machine, find minimum button presses needed.
    Each button affects multiple positions when pressed.
    Need all positions to reach exact target values.
    """
    # Parse input, for all machines
    all_requirements = []  # Target values for each position
    all_wiring_schematics = []  # Which positions each button affects

    for line in lines:  # Elements are already split on groups (spaces)
        # Last element:requirements  like "[5,3,7]"
        all_requirements.append(list(map(int, line[-1][1:-1].split(','))))

        # Middle elements: button effects like "(0,2)" "(1,3,4)"
        sws = [sw[1:-1].split(',') for sw in line[1:-1]]
        all_wiring_schematics.append(tuple([(tuple(map(int, sw))) for sw in sws]))

    res = 0

    # Solve each machine independently
    for requirements, schematics in zip(all_requirements, all_wiring_schematics):
        s = Optimize()  # Z3 optimizer (can minimize objectives)
        # s = Solver()  # Basic solver (just finds feasible solution)

        # Create integer variable for each button (number of times pressed)
        alist = [Int('a%s' % i) for i in range(len(schematics))]

        # Constraint: all buttons pressed non-negative times
        for a in alist:
            s.add(a >= 0)

        # Build equations: one per position in requirement
        # eqs[i] will be the sum of button presses affecting position i
        eqs = [None] * len(requirements)

        # For each button, add its contribution to affected positions
        for buttom_idx, buttom_wiring in enumerate(schematics):
            for idx in buttom_wiring:  # idx = position this button affects
                if eqs[idx] is None:
                    eqs[idx] = alist[buttom_idx]  # First button affecting this position
                else:
                    eqs[idx] = eqs[idx] + alist[buttom_idx]  # Add to existing

        # Constraint: each position must equal its target value
        for idx, requirement in enumerate(requirements):
            eqs[idx] = eqs[idx] == requirement

        # Add all equality constraints
        for eq in eqs:
            s.add(eq)

        # Objective: minimize total button presses
        s.minimize(sum(alist))

        # Solve and extract solution
        s.check()
        f = s.model()

        # Sum button presses for this machine
        res += (sum([f[a].as_long() for a in alist]))

    print("Part 2: ", res)

part2()

# Not working solutions

@cache
def find_path(state, target, switch):
    if state == target:
        return 0

    dists = [float('inf')]
    for sw in switch:
        new_state = list(state)
        valid = True
        for idx in sw:
            if new_state[idx] + 1 <= target[idx]:
                new_state[idx] += 1
            else:
                valid = False
                break
        if valid:
            dists.append(find_path(tuple(new_state), target, switch))
    return min(dists)+1


# To slow for real dataset,  even as we have cache
def part2_DFS():
    res = 0
    kk = 0
    for target, switch in zip(targets, switches):
        kk += 1
        print(kk)
        target = tuple(target)
        inital_state = tuple([0]*len(target))
        res += find_path(inital_state, target, switch)
    print(res)


# part 2 BFS way to slow
def part2_BFS():
    kk = 0
    res = 0
    for target, switch in zip(targets, switches):
        kk += 1
        print(kk)
    #target = targets[0]
    #switch = switches[0]
        queue = deque()
        inital_state = [0]*len(target)
        queue.append([inital_state, 0])
        while queue:
            state, N = queue.popleft()

            if state == target:
                res += N
                print(N)
                break

            for sw in switch:
                new_state = state.copy()
                valid = True
                for idx in sw:
                    if new_state[idx] + 1 <= target[idx]:
                        new_state[idx] += 1
                    else:
                        valid = False
                        break                
                if valid: queue.append([new_state, N + 1])
    print("Part 2: ", res)
