# Multiple groups, returned as a list of lists of strings
with open('../data/12_data.dat') as f:
    groups = [group.splitlines() for group in f.read().split('\n\n')]

# loader and unpack data
Nshapes = 6  # Same for test and real data
shapes = {}
for kk in range(Nshapes):
    shapes[kk] = groups[kk][1:]

regions = []
for lines in groups[-1]:
    size, quantity = lines.split(':')
    regions.append([tuple(map(int, size.split('x'))),
                    list(map(int, quantity.split()))])


# lets take a wild guess, that if the shapes take up less space than needed
def part1():
    res = 0
    for region in regions:
        A = region[0][0]*region[0][1]
        Nfill = 0
        for shape_id, N_shape in enumerate(region[1]):
            Nfill_shape = 0
            for line in shapes[shape_id]:
                Nfill_shape += line.count('#')
            Nfill += N_shape * Nfill_shape
        if Nfill <= A:
            res += 1

    print("Part 1: ", res)


part1()
