from collections import deque 

#with open('../data/10_testdata.dat') as f:
with open('../data/10_data.dat') as f:
    lines = [x.strip().split() for x in f]


def sw_to_num(sw):
    num = 0
    for bit in sw:
        num += 2**bit
    return num


# Unpacking is a bit evolved today, convert to base 10 number representation
targets = []
switches = []
switches_num = []
for line in lines:
    targets.append(int(line[0][1:-1].replace('.','0').replace('#','1')[::-1],2))
    sws = [sw[1:-1].split(',') for sw in  line[1:-1]]
    switches.append([sw_to_num(list(map(int,sw)))  for sw in sws])

def part1():
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
part1()
