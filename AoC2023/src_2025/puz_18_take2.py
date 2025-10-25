#with open('../testdata/18_testdata.dat') as f:
with open('../data/18_data.dat') as f:
    plan=[x.strip().split(' ') for x in f]


# Coordinate are given as (line, column)

#label to direction dict for part 1
dirs1 = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

# label to direction dict for part 2
dirs2 = {'3': (-1, 0), '1': (1, 0), '2': (0, -1), '0': (0, 1)}


def CalculateNtot(corners):
    # Use the "Trapezoid formula" for area (https://en.wikipedia.org/wiki/Shoelace_formula)
    # and Calculate number of edge points
    A = 0
    Nedge = 0
    for n in range(len(corners)-1):
        A += (corners[n][1]+corners[n+1][1])*(corners[n][0]-corners[n+1][0])*0.5
        Nedge += abs(corners[n][1]-corners[n+1][1]) + abs(corners[n][0]-corners[n+1][0]) 

    # use Pick's theorem (https://en.wikipedia.org/wiki/Pick%27s_theorem) (thanks claude.ai)
    # A = Nint + Nedge/2 - 1 ->  Ntot = Nint + Nedge = A + 1 + Nedge/2 
    A = abs(A)
    print(int(A+1+Nedge/2))



# part 1
def part1():

    # Arbitrary start point
    pos = (0, 0)
    corners = [] 
    corners.append(pos)

    # calculate and store the visited corners
    for dig in plan:
        dir, num, color = dig
        num = int(num) 
        pos = (pos[0] + dirs1[dir][0] * num, pos[1] + dirs1[dir][1] * num)
        corners.append(pos)

    # Calculate the result
    CalculateNtot(corners)

part1()

# part 2
def part2():

    # Arbitrary start point
    pos = (0, 0)
    corners = [] 
    corners.append(pos)

    # calculate and store the visited corners
    for dig in plan:
        _, _, color = dig
        num = int(color[2:-2],16)
        dir = (color[-2]) 
        pos = (pos[0] + dirs2[dir][0] * num, pos[1] + dirs2[dir][1] * num)
        corners.append(pos)

    # Calculate the result
    CalculateNtot(corners)

part2()
