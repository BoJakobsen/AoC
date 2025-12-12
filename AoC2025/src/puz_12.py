import matplotlib.pyplot as plt

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
    DegreeFill = []
    res = 0
    for region in regions:
        A = region[0][0]*region[0][1]
        Nfill = 0
        for shape_id, N_shape in enumerate(region[1]):
            Nfill_shape = 0
            for line in shapes[shape_id]:
                Nfill_shape += line.count('#')
            Nfill += N_shape * Nfill_shape
        DegreeFill.append((Nfill / A)*100)
        if Nfill <= A:
            res += 1

    print("Part 1: ", res)
    return DegreeFill

DegreeFill = part1()


# Plot histogram of DegreeFill with <100% highlighted in red
plt.figure(figsize=(10, 6))
# Separate data into <100 and >=100
below_100 = [x for x in DegreeFill if x < 100]
above_100 = [x for x in DegreeFill if x >= 100]

# Create bins with 100% as a clear boundary
bins = list(range(50, 100, 2)) + [100, 101]

plt.hist(below_100, bins=bins, color='blue', alpha=0.7, edgecolor='black', label='< 100%')
plt.hist(above_100, bins=bins, color='red', alpha=0.7, edgecolor='black', label='>= 100%')
plt.axvline(100, color='black', linestyle='--', linewidth=2, label='100% threshold')
plt.xlabel('Degree of Fill (%)')
plt.ylabel('Frequency')
plt.title('Histogram of DegreeFill')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
