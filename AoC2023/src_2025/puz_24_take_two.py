# Version with comments by Claude.ai

import sympy as sp
import numpy

# ============================================================================
# DATA LOADING (Used for both parts)
# ============================================================================

#with open('../testdata/24_testdata.dat') as f:
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
# PART 2: Find rock trajectory that hits all hailstones
# ============================================================================
# Strategy: Set up system of 9 equations with 9 unknowns
# - 6 unknowns: Rock's initial position (Xr) and velocity (Vr) in 3D
# - 3 unknowns: Times (t[i]) when rock hits each of first 3 hailstones
# 
# For each hailstone i at time t[i]:
# - Rock position: Xr + Vr * t[i]
# - Hailstone position: coords[i] + vels[i] * t[i]
# - These must be equal (collision)
#
# This gives 3 vector equations (x, y, z components) × 3 hailstones = 9 equations


def part2():
    Neq = 3  # Number of hailstones to use (gives 3 vector equations = 9 scalar equations)

    # Define symbolic variables for unknowns
    t = [sp.Symbol(f't{i}', positive=True) for i in range(Neq)]  # Collision times for each hailstone
    Xr = [sp.Symbol(f'Xr{j}', positive=True) for j in range(3)]  # Rock's initial position (x, y, z)
    Vr = [sp.Symbol(f'Vr{j}') for j in range(3)]  # Rock's velocity (vx, vy, vz)

    # Collect all unknowns into single tuple for solver
    unknowns = tuple(t + Xr + Vr)  # (t0, t1, t2, Xr0, Xr1, Xr2, Vr0, Vr1, Vr2)

    # Generate equations: For each hailstone and each coordinate (x, y, z)
    # Equation: hailstone_pos[i][j] + hailstone_vel[i][j]*t[i] = Xr[j] + Vr[j]*t[i]
    # This says: "At time t[i], rock and hailstone i are at same position"
    eqs = []
    for i in range(Neq):  # For each of the 3 hailstones
        for j in range(3):  # For each coordinate (x=0, y=1, z=2)
            # Position of hailstone i at time t[i] equals position of rock at time t[i]
            eqs.append(sp.Eq(coords[i][j] + vels[i][j]*t[i], Xr[j]+Vr[j]*t[i]))

    # Solve the system of 9 equations in 9 unknowns
    # Returns list of solution dictionaries
    res = sp.solve(eqs, unknowns, dict=True)

    # Calculate answer: sum of rock's initial x, y, z coordinates
    res_part2 = 0
    for i in range(3):
        res_part2 += res[0][Xr[i]]  # res[0] = first (and only) solution

    print(f"Part 2: {res_part2}")


part2()


# ============================================================================
# PART 2, fully algebraic version (experimental - doesn't complete)
# ============================================================================
# This version keeps hailstone positions/velocities as symbolic variables
# instead of substituting numerical values. More general but much slower.

def part2_full_alg():
    Neq = 3  # Number of equations

    # Define symbolic variables for unknowns
    t = [sp.Symbol(f't{i}', positive=True) for i in range(Neq)]  # Collision times for each hailstone
    Xr = [sp.Symbol(f'Xr{j}', positive=True) for j in range(3)]  # Rock's initial position (x, y, z)
    Vr = [sp.Symbol(f'Vr{j}') for j in range(3)]  # Rock's velocity (vx, vy, vz)

    # Collect all unknowns into single tuple for solver
    unknowns = tuple(t + Xr + Vr)  # (t0, t1, t2, Xr0, Xr1, Xr2, Vr0, Vr1, Vr2)

    # Keep hailstone data as symbolic variables (not concrete numbers)
    # Xh[i][j] = position of hailstone i, coordinate j
    Xh = [[sp.Symbol(f'Xh{i}{j}', positive=True) for j in range(3)] for i in range(Neq)]
    # Vh[i][j] = velocity of hailstone i, coordinate j
    Vh = [[sp.Symbol(f'Vh{i}{j}') for j in range(3)] for i in range(Neq)]

    # Generate equations with symbolic hailstone data
    eqs = []
    for i in range(Neq):
        for j in range(3):
            # Symbolic version: Xh and Vh are variables, not concrete values
            eqs.append(sp.Eq(Xh[i][j] + Vh[i][j] * t[i], Xr[j] + Vr[j] * t[i]))

    # Attempt to solve symbolically (warning: very slow/doesn't complete)
    # This would give a general formula in terms of Xh and Vh
    # res_alg = sp.solve(eqs, unknowns, dict=True)
    # Note: Too computationally expensive - system is too complex for symbolic solution

