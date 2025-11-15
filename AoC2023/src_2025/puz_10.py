#single block of data
#with open('../testdata/10_2_testdata.dat') as f:
with open('../data/10_data.dat') as f:
    grid=[x.strip() for x in f]


Nrow = len(grid)
Ncol = len(grid[0])

for row, line in enumerate(grid):
    if 'S' in line:
        start = (row, line.index('S'))

# setup some dicts for converting symbols and directions.
pipes_connecting = {'|': 'NS', '-': 'EW', 'L': 'NE', 'J': 'NW', '7': 'SW',
                    'F': 'SE', 'S': 'NSEW'}
dirs = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}


def part1():

    # count distance around the loop, tracking along the pipes.
    visited = [] # set is much faster, but part 2 needs the list
    cur_pos = start
    while True:
        visited.append(cur_pos)
        pipe = grid[cur_pos[0]][cur_pos[1]]
    #    print(cur_pos,pipe)
        for dir in pipes_connecting[pipe]:
            test_pos = (cur_pos[0] + dirs[dir][0], cur_pos[1] + dirs[dir][1])
            if len(visited) > 2 and test_pos == start:
                break
            if test_pos[0] not in range(Nrow) or test_pos[1] not in range(Ncol):
                continue
            if test_pos in visited:
                continue
            test_pipe = grid[test_pos[0]][test_pos[1]]
            if test_pipe == '.':
                continue
            connects_back = False
            for test_dir in pipes_connecting[test_pipe]:
                test_back_pos = (test_pos[0] + dirs[test_dir][0],
                                 test_pos[1] + dirs[test_dir][1])
                if test_back_pos == cur_pos:
                    connects_back = True
                    break
            if connects_back:
                cur_pos = test_pos
                break
        if test_pos == start:
            break

    # should be OK independent of even of uneven number of steps. 
    print(len(visited)/2)
    return visited

# Solvepart one, and get the boundary
boundery = part1()



# For second part "S" needs to be changed to the correct
# pipe,

print(boundery[1])  # (61, 111), 7
print(start)        # (62, 111)
print(boundery[-1]) # (62, 110)  -
# Which draws to : 
#       7
#      -S

# so in this case S must be a North West : J
# manually change the grid, now very nice
grid[start[0]] = grid[start[0]].replace('S', 'J')

# Convert list to set for speed
boundery = set(boundery)


def part2():
    ins = set()
    # find points on the inside, by a Ray Cast method.
    Ninside = 0
    for r in range(0,Nrow):
        for c in range(1,Ncol-1):
            if (r, c) in boundery:
                continue
            crossings = 0
            for c_test in range(c+1, Ncol):
                test_point = (r, c_test)
                test_pipe = grid[r][c_test]
                if test_point in boundery:
                    #print(crossings)
                    #print(test_point, test_pipe)
                    if test_pipe == '-':
                        continue
                    if (test_point[0], test_point[1]-1) not in boundery:
                        crossings += 1
                        continue
                    n = 1
                    while grid[test_point[0]][test_point[1]-n] == '-':
                        n += 1
                    prew_pipe = grid[test_point[0]][test_point[1]-n]
                    if (('E' not in pipes_connecting[prew_pipe]) or
                           ('W' not in pipes_connecting[test_pipe])):
                        crossings += 1
                        continue
                    if (('N' in pipes_connecting[prew_pipe]) and
                           ('N' in pipes_connecting[test_pipe])):
                        crossings += 1
                        continue
                    if (('S' in pipes_connecting[prew_pipe]) and
                           ('S' in pipes_connecting[test_pipe])):
                        crossings += 1
                        continue
            if crossings % 2 == 1:
                Ninside += 1
                ins.add((r, c))

    print(Ninside)
    return ins

_ = part2()
