from z3 import Optimize, Int
from functools import cache
from collections import deque 

#with open('../data/10_testdata.dat') as f:
with open('../data/10_data.dat') as f:
    lines = [x.strip().split() for x in f]


def sw_to_num(sw):
    num = 0
    for bit in sw:
        num += 2**bit
    return num



def part1():

    # Unpacking is a bit evolved today, convert to base 10 number representation
    # was only good for part 1
    targets = []
    switches = []
    for line in lines:
        targets.append(int(line[0][1:-1].replace('.','0').replace('#','1')[::-1],2))
        sws = [sw[1:-1].split(',') for sw in  line[1:-1]]
        switches.append([sw_to_num(list(map(int,sw)))  for sw in sws])

    res = 0
    for target, switch in zip(targets, switches):
        queue = deque()
        queue.append([0, 0])
        while queue:
            state, N = queue.popleft()
            if state == target:
                res += N
                break

            for sw in switch:
                queue.append([state ^ sw, N + 1])

    print("Part 1: ", res)


# part 1 is a bit slow, but reasonable
#part1()


# Part 2 using Z3 solver
def part2():
    # need simpler data structure
    targets = []
    switches = []
    for line in lines:
        targets.append(list(map(int, line[-1][1:-1].split(','))))
        sws = [sw[1:-1].split(',') for sw in line[1:-1]]
        switches.append(tuple([(tuple(map(int, sw))) for sw in sws]))


    res = 0
    for target, switch in zip(targets, switches):
        s = Optimize()
        # s = Solver()

        # generate the integer unknowns
        alist = [Int('a%s' % i) for i in range(len(switch))]

        # add restrictions a > 0
        for a in alist:
            s.add(a >= 0)

        # setup the equations, one for each number in target.
        eqs = [None]*len(target)

        # generate array of equations
        for swidx, sw in enumerate(switch):
            for idx in sw:
                if eqs[idx] is None:
                    eqs[idx] = alist[swidx]
                else:
                    eqs[idx] = eqs[idx] + alist[swidx]

        for idx, ta in enumerate(target):
            eqs[idx] = eqs[idx] == ta

        for eq in eqs:
            s.add(eq)

        # we want a minimal solution
        s.minimize(sum(alist))

        # solve / minimize 
        s.check()
        f = s.model()
        # sum the found coefficients
        res += (sum([f[a].as_long() for a in alist]))

    print(res)


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
