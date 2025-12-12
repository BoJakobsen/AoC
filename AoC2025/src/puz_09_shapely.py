# Solution suggested by Claude.ai during
# code review for my "ray-cast" solution.
# Still not fast but properly way more robust.

from shapely.geometry import Polygon, box

#with open('../data/09_testdata.dat') as f:
with open('../data/09_data.dat') as f:
    rtiles = [list(map(int, x.strip().split(','))) for x in f]
    # Coordinates: x is horizontal (right), y is vertical (down)


def calc_area(t1, t2):
    """Calculate area of rectangle defined by two corner points."""
    return (abs(t1[0]-t2[0])+1)*(abs(t1[1]-t2[1])+1)


# Generate all candidate rectangles (pairs of vertices)
rectangles = []
for kk in range(len(rtiles)):
    for ll in range(kk+1, len(rtiles)):
        rectangles.append([rtiles[kk], rtiles[ll]])

# Use shapely to test all possible rectangles. 
areas = []
polygon = Polygon(rtiles)
for c1, c2 in rectangles:
    rect = box(min(c1[0],c2[0]), min(c1[1],c2[1]), 
               max(c1[0],c2[0]), max(c1[1],c2[1]))
    if polygon.contains(rect):
        # Valid rectangle
        areas.append(calc_area(c1,c2))

print("Part 2: ", max(areas))

