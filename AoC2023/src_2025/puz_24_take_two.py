# Version with comments by Claude.ai

import sympy as sp
import numpy

# ============================================================================
# DATA LOADING (Used for both parts)
# ============================================================================

#with open('testdata/24_testdata.dat') as f:
with open('../data/24_data.dat') as f:
    lines = [x.strip() for x in f]

# Parse hailstone positions and velocities
# Input format: "px, py, pz @ vx, vy, vz"
coords = []  # Initial positions [x, y, z]
vels = []    # Velocities [vx, vy, vz]

for line in lines:
    coordstr, velstr = line.split('@')
    coord = list(map(int, coordstr.split(',')))
    vel = list(map(int, velstr.split(',')))
    coords.append(coord)
    vels.append(vel)

# ============================================================================
# Symbolic equations for part 1,
# this is rather overkill but a nice exercise on using sympy
# ============================================================================

# Symbolic variables for two hailstone intersections
t1, t2 = sp.symbols('t1 t2')      # Time variables.
x1, v1 = sp.symbols('x1 v1')      # Position, time, x-velocity for hailstone 1
x2, v2 = sp.symbols('x2 v2')      # Position, time, x-velocity for hailstone 2
y1, w1 = sp.symbols('y1 w1')      # Y-position, y-velocity for hailstone 1
y2, w2 = sp.symbols('y2 w2')      # Y-position, y-velocity for hailstone 2

# Position equations: position = initial_position + time * velocity
# X-coordinate equations
eq1_1 = sp.sympify(x1 + t1 * v1)  # Hailstone 1 x-position at time t1
eq1_2 = sp.sympify(x2 + t2 * v2)  # Hailstone 2 x-position at time t2

# Y-coordinate equations
eq2_1 = sp.sympify(y1 + t1 * w1)  # Hailstone 1 y-position at time t1
eq2_2 = sp.sympify(y2 + t2 * w2)  # Hailstone 2 y-position at time t2

# Set up equations for finding intersection times t1 and t2
# When do the two trajectories intersect?
eq1 = sp.Eq(eq1_1, eq1_2)  # X-coordinates equal at intersection
eq2 = sp.Eq(eq2_1, eq2_2)  # Y-coordinates equal at intersection

# Solve for t1 and t2 (times when paths intersect)
res = sp.solve([eq1, eq2], (t1, t2), dict=True)

# Equation for intersection point (substitute t1 back into position equations)
xeq = eq1_1.subs(t1, res[0][t1])  # X-coordinate of intersection
yeq = eq2_1.subs(t1, res[0][t1])  # Y-coordinate of intersection

# Convert symbolic equations to fast numpy functions for evaluation
xeqf = sp.lambdify([x1, y1, v1, w1, x2, y2, v2, w2], xeq, "numpy")
yeqf = sp.lambdify([x1, y1, v1, w1, x2, y2, v2, w2], yeq, "numpy")
t1eqf = sp.lambdify([x1, y1, v1, w1, x2, y2, v2, w2], res[0][t1], "numpy")
t2eqf = sp.lambdify([x1, y1, v1, w1, x2, y2, v2, w2], res[0][t2], "numpy")


# ============================================================================
# PART 1: Count intersections within test area (2D projection, ignore Z)
# ============================================================================

# Test area boundaries (2D: only X and Y coordinates)
MIN = 200000000000000
MAX = 400000000000000


def part1():
    cnt = 0  # Count of valid intersections

    # Check all pairs of hailstones for 2D path intersections
    for k in range(len(coords)):
        for kk in range(k + 1, len(coords)):  # Only check each pair once
            coord1 = coords[k]   # Starting position of hailstone 1
            vel1 = vels[k]       # Velocity of hailstone 1
            coord2 = coords[kk]  # Starting position of hailstone 2
            vel2 = vels[kk]      # Velocity of hailstone 2

            # Check if paths are parallel (same slope in XY plane)
            if vel1[0] / vel1[1] == vel2[0] / vel2[1]:
                continue
                # print(k, kk, 'Parallel')
            else:
                # Calculate intersection point and times using symbolic functions
                t1 = t1eqf(coord1[0], coord1[1], vel1[0], vel1[1],
                           coord2[0], coord2[1], vel2[0], vel2[1])
                t2 = t2eqf(coord1[0], coord1[1], vel1[0], vel1[1],
                           coord2[0], coord2[1], vel2[0], vel2[1])
                x = xeqf(coord1[0], coord1[1], vel1[0], vel1[1],
                         coord2[0], coord2[1], vel2[0], vel2[1])
                y = yeqf(coord1[0], coord1[1], vel1[0], vel1[1],
                         coord2[0], coord2[1], vel2[0], vel2[1])

                # Check if intersection is valid
                if t1 < 0 or t2 < 0:
                    # Intersection happened in the past for at least one hailstone
                    # print(k, kk, 'in Past')
                    continue
                elif x < MIN or x > MAX or y < MIN or y > MAX:
                    # Intersection outside test area
                    # print(k, kk, x, y, 'OUTSIDE')
                    continue
                else:
                    # Valid intersection: in future and within test area
                    # print(k, kk, x, y, 'OK')
                    cnt += 1

    print('Intersecting paths: ', cnt)  # Part 1 answer


part1()

# ============================================================================
# PART 2 SETUP (Not used in Part 1 solution below)
# ============================================================================
# Setup symbolic algebra for finding rock trajectory that hits all hailstones
# This approach sets up equations but isn't completed/used yet
