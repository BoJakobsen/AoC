#single block of data
#with open('../testdata/10_testdata.dat') as f:
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
    visited = set()
    cur_pos = start
    while True:
        visited.add(cur_pos)
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

part1()
