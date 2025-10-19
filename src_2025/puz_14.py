import re
from timeit import default_timer as timer
#
#with open('../testdata/14_testdata.dat') as f:
with open('../data/14_data.dat') as f:
    lines=[list(x.strip()) for x in f]


# Move round stones as fare as possible to the left 
def move_left(lines_f):
    for k in range(len(lines_f)):
        line_f_str = "".join(list(lines_f[k]))
        O_pos = [match.start() for match in re.finditer(r'O', line_f_str)]
        B_pos = [match.start() for match in re.finditer(r'#', line_f_str)]

        line = list(lines_f[k])
        B_pos.append(len(line))  # Put a block way to the right fixes edge cases
        b_index = 0
        ind_block_index = 0
        for O in O_pos:
            line[O] = "."  # works if we assume the list is from small to large
            if O > B_pos[b_index]:  # We are to the right of current cube
                while O > B_pos[b_index]:  # find next ok block of free space
                    b_index += 1
                ind_block_index = 0  # must be first rolling block
            if b_index == 0:  # moving to the very right 
                line[ind_block_index] = 'O'
            else:
                line[B_pos[b_index-1]+ind_block_index+1] = 'O'
            ind_block_index += 1
        lines_f[k] = line


# Clockwise rotation
def cw_rot(lines_f):
    return [list(row) for row in zip(*lines_f[::-1])]

# Counter clockwise rotation
def ccw_rot(lines_f):  # counter clockwise
    return list(zip(*lines_f))[::-1]


# Solve part 1
def part1():
    lines_f = lines.copy()
    # One cc rotation to bring north to the left
    lines_f = ccw_rot(lines_f)
    move_left(lines_f)

    # this counting still assumes North to the left.
    res = 0
    for line in lines_f:
        for id, ch in enumerate(line):
            if ch == 'O':
                res += len(line) - id
    print(res)


part1()

# Define the spin cycle
def cycle(lines_f):
    # North
    move_left(lines_f)

    # West
    lines_f = cw_rot(lines_f)
    move_left(lines_f)

    # South
    lines_f = cw_rot(lines_f)
    move_left(lines_f)

    # East
    lines_f = cw_rot(lines_f)
    move_left(lines_f)

    # back to north
    lines_f = cw_rot(lines_f)

    return lines_f


def printit(lines_f):
    for line in lines_f:
        print(line)
    print()

    
# run 3 cycle on the test data for comparing to problem formulation 
def part2_test():
    lines_f = lines.copy()

    printit(lines_f)
    for kk in range(0,3):
        # rotate North back and forward for printing upright 
        lines_f = ccw_rot(lines_f)
        lines_f = cycle(lines_f)
        lines_f = cw_rot(lines_f)
        printit(lines_f)


# part2_test()

# Make N cycles no printout for timing
def part2_test2(N):
    #  copy and make one counter clocwise rotation to bring northe to the left
    lines_f = lines.copy()
    lines_f = ccw_rot(lines_f)

    for kk in range(0,N):
        lines_f = cycle(lines_f)
    lines_f = cw_rot(lines_f)


# Time it
# start = timer()
# part2_test2(1000)
# end = timer()
# print(end - start) # Time in seconds, e.g.
# 0.35 s for 1000 on test data so 1000.000.000 is our of the question this way
# 7.7 s for 1000 on real data so 1000.000.000 is our of the question this way


def part2():
    # Looking for a cycle requires a non-mutable key.
    def matrix_to_key(matrix):
        """Convert matrix to hashable tuple"""
        return tuple(tuple(row) for row in matrix)


    #  Make one counter clocwise rotation to bring northe to the left
    lines_f = lines.copy()
    lines_f = ccw_rot(lines_f)

    # Look for a cycle (if this does not exits this will not end in reasonable time)
    seenstates = {}
    N = 1000_000_000
    for kk in range(0,N):
        key = matrix_to_key(lines_f)
        if key in seenstates:
            print('Cycle found', seenstates[key], kk)
            Nstart = seenstates[key]
            Ncyc = kk - seenstates[key]
            CycState = key
            break
        seenstates[key] = kk
        lines_f = cycle(lines_f)

    # Perform missing cycles for N in total skipping integer numbers of cycles 
    for kk in range(0, (N-kk) % Ncyc):
        lines_f = cycle(lines_f)

    # Count the "load on the north beam"
    res = 0
    for line in lines_f:
        for id, ch in enumerate(line):
            if ch == 'O':
                res += len(line) - id
    print(res)

part2()
