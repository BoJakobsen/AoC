from collections import defaultdict

#with open('../data/09_testdata.dat') as f:
with open('../data/09_data.dat') as f:
    rtiles = [list(map(int, x.strip().split(','))) for x in f]
    # x , y (where x it to the right, and y is downwards)


def calc_area(t1, t2):
    return (abs(t1[0]-t2[0])+1)*(abs(t1[1]-t2[1])+1)


def part1():
    arears = []
    kk = 0
    for kk in range(len(rtiles)):
        for ll in range(kk-1, len(rtiles)):
            arears.append([calc_area(rtiles[kk],
                                     rtiles[ll]), rtiles[kk], rtiles[ll]])

    print('Part 1: ', max(arears)[0])


part1()


# map all edges
v_edges = defaultdict(list)
h_edges = defaultdict(list)
last_tile = rtiles[-1]
for tile in rtiles:
    if last_tile[0] == tile[0]:  # vertical edge
        v_edges[last_tile[0]] = sorted([last_tile[1], tile[1]])
    else:  # horizontal edge
        h_edges[last_tile[1]] = sorted([last_tile[0], tile[0]])
    last_tile = tile


# precalculate all rectangles
rectangles = []
for kk in range(len(rtiles)):
    for ll in range(kk+1, len(rtiles)):
        rectangles.append([rtiles[kk], rtiles[ll]])


def check_top(p1, p2):  # horizontal line in top
    idxs = [key for key in v_edges.keys() if key > min([p1[0], p2[0]]) and
            key < max([p1[0], p2[0]])]
    for idx in idxs:
        if p1[1] >= v_edges[idx][0] and p1[1] < v_edges[idx][1]:
            return False
    return True


def check_bot(p1, p2):  # horizontal line in bottom
    idxs = [key for key in v_edges.keys() if key > min([p1[0], p2[0]]) and
            key < max([p1[0], p2[0]])]
    for idx in idxs:
        if p1[1] > v_edges[idx][0] and p1[1] <= v_edges[idx][1]:
            return False
    return True


def check_left(p1, p2):  # vertical line to the left
    idxs = [key for key in h_edges.keys() if key > min([p1[1], p2[1]]) and
            key < max([p1[1], p2[1]])]
    for idx in idxs:
        if p1[0] >= h_edges[idx][0] and p1[0] < h_edges[idx][1]:
            return False
    return True


def check_right(p1, p2):  # vertical line to the right
    idxs = [key for key in h_edges.keys() if key > min([p1[1], p2[1]]) and
            key < max([p1[1], p2[1]])]
    for idx in idxs:
        if p1[0] > h_edges[idx][0] and p1[0] <= h_edges[idx][1]:
            return False
    return True


def test_rect(c1, c2):
    top_left = (min([c1[0], c2[0]]), min([c1[1], c2[1]]))
    top_right = (max([c1[0], c2[0]]), min([c1[1], c2[1]]))
    bot_left = (min([c1[0], c2[0]]), max([c1[1], c2[1]]))
    bot_right = (max([c1[0], c2[0]]), max([c1[1], c2[1]]))
    a = check_top(top_left, top_right)
    b = check_bot(bot_left, bot_right)
    c = check_left(top_left, bot_left)
    d = check_right(top_right, bot_right)
    return a and b and c and d


def part2():
    sizes = []
    for c1, c2 in rectangles:
        if test_rect(c1, c2):
            sizes.append(calc_area(c1, c2))
    print("Part 2: ", max(sizes))


part2()
