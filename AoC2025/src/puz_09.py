from collections import defaultdict
#with open('../data/09_testdata.dat') as f:
with open('../data/09_data.dat') as f:
    rtiles = [list(map(int, x.strip().split(','))) for x in f]
    # Coordinates: x is horizontal (right), y is vertical (down)


def calc_area(t1, t2):
    """Calculate area of rectangle defined by two corner points."""
    return (abs(t1[0]-t2[0])+1)*(abs(t1[1]-t2[1])+1)


def part1():
    """Find largest rectangle between any two polygon vertices (ignoring containment)."""
    arears = []
    kk = 0
    for kk in range(len(rtiles)):
        for ll in range(kk-1, len(rtiles)):
            arears.append([calc_area(rtiles[kk],
                                     rtiles[ll]), rtiles[kk], rtiles[ll]])
    print('Part 1: ', max(arears)[0])


part1()

# Build edge map from polygon vertices
# v_edges[x] = [y_min, y_max] for vertical edge at x-coordinate
# h_edges[y] = [x_min, x_max] for horizontal edge at y-coordinate
# NB! assumes only one vertical edge per x coordinate, and likewise for y,
# works for my input, might not be general.
v_edges = defaultdict(list)
h_edges = defaultdict(list)
last_tile = rtiles[-1]

for tile in rtiles:
    # Connect consecutive vertices to form edges
    if last_tile[0] == tile[0]:  # Same x = vertical edge
        v_edges[last_tile[0]] = sorted([last_tile[1], tile[1]])
    else:  # Different x = horizontal edge
        h_edges[last_tile[1]] = sorted([last_tile[0], tile[0]])
    last_tile = tile

# Generate all candidate rectangles (pairs of vertices)
rectangles = []
for kk in range(len(rtiles)):
    for ll in range(kk+1, len(rtiles)):
        rectangles.append([rtiles[kk], rtiles[ll]])


def check_top(p1, p2):
    """Check if top horizontal edge of rectangle crosses any vertical polygon edges.

    Returns False if a polygon edge crosses into the interior of the rectangle.
    """
    # Find vertical edges between left and right x-coords of rectangle
    idxs = [key for key in v_edges.keys() if key > min([p1[0], p2[0]]) and
            key < max([p1[0], p2[0]])]

    # Check if top y-coordinate falls within any vertical edge span
    for idx in idxs:
        if p1[1] >= v_edges[idx][0] and p1[1] < v_edges[idx][1]:
            return False  # Crosses a polygon edge
    return True


def check_bot(p1, p2):
    """Check if bottom horizontal edge crosses any vertical polygon edges."""
    idxs = [key for key in v_edges.keys() if key > min([p1[0], p2[0]]) and
            key < max([p1[0], p2[0]])]
    for idx in idxs:
        if p1[1] > v_edges[idx][0] and p1[1] <= v_edges[idx][1]:
            return False
    return True


def check_left(p1, p2):
    """Check if left vertical edge crosses any horizontal polygon edges."""
    idxs = [key for key in h_edges.keys() if key > min([p1[1], p2[1]]) and
            key < max([p1[1], p2[1]])]
    for idx in idxs:
        if p1[0] >= h_edges[idx][0] and p1[0] < h_edges[idx][1]:
            return False
    return True


def check_right(p1, p2):
    """Check if right vertical edge crosses any horizontal polygon edges."""
    idxs = [key for key in h_edges.keys() if key > min([p1[1], p2[1]]) and
            key < max([p1[1], p2[1]])]
    for idx in idxs:
        if p1[0] > h_edges[idx][0] and p1[0] <= h_edges[idx][1]:
            return False
    return True


def test_rect(c1, c2):
    """Test if rectangle defined by two corners is entirely within polygon.

    Checks all 4 sides to ensure none cross polygon edges (ray-casting approach).
    """
    # Determine rectangle corners from two arbitrary vertices
    top_left = (min([c1[0], c2[0]]), min([c1[1], c2[1]]))
    top_right = (max([c1[0], c2[0]]), min([c1[1], c2[1]]))
    bot_left = (min([c1[0], c2[0]]), max([c1[1], c2[1]]))
    bot_right = (max([c1[0], c2[0]]), max([c1[1], c2[1]]))

    # Check all four sides
    a = check_top(top_left, top_right)
    b = check_bot(bot_left, bot_right)
    c = check_left(top_left, bot_left)
    d = check_right(top_right, bot_right)

    return a and b and c and d  # All sides must be valid


def part2():
    """Find largest rectangle with corners at polygon vertices that fits inside polygon."""
    sizes = []
    for c1, c2 in rectangles:
        if test_rect(c1, c2):
            sizes.append(calc_area(c1, c2))
    print("Part 2: ", max(sizes))


part2()
