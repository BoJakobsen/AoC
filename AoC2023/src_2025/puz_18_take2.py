# Added comments by claude.ai

# Day 18: Calculate area of polygon defined by digging instructions
# Part 1: Use direction and distance from columns 1-2
# Part 2: Extract direction and distance from hex color code

#with open('../testdata/18_testdata.dat') as f:
with open('../data/18_data.dat') as f:
    plan=[x.strip().split(' ') for x in f]  # Parse: ['R', '6', '(#70c710)']

# Coordinate system: (row, column) where row increases downward
# Label to direction dict for part 1
dirs1 = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

# Label to direction dict for part 2 (from last digit of hex color)
# Hex digit mapping: 0=R, 1=D, 2=L, 3=U
dirs2 = {'3': (-1, 0), '1': (1, 0), '2': (0, -1), '0': (0, 1)}

def CalculateNtot(corners):
    """
    Calculate total number of grid points (interior + boundary) in polygon.
    Uses Shoelace formula + Pick's theorem.
    
    Args:
        corners: List of (row, col) tuples defining polygon vertices
    """
    # Use the "Trapezoid formula" for area (https://en.wikipedia.org/wiki/Shoelace_formula)
    # Calculates signed area of polygon from vertices
    A = 0
    
    # Calculate number of edge points (perimeter length)
    Nedge = 0
    
    # Sum contributions from each edge
    for n in range(len(corners)-1):
        # Shoelace: sum of (y_i + y_{i+1}) * (x_i - x_{i+1})
        A += (corners[n][1]+corners[n+1][1])*(corners[n][0]-corners[n+1][0])*0.5
        
        # Manhattan distance between consecutive corners = boundary points on this edge
        Nedge += abs(corners[n][1]-corners[n+1][1]) + abs(corners[n][0]-corners[n+1][0]) 
    
    # Use Pick's theorem (https://en.wikipedia.org/wiki/Pick%27s_theorem) (thanks claude.ai)
    # Pick's: A = N_interior + N_boundary/2 - 1
    # Rearranging: N_total = N_interior + N_boundary = A + N_boundary/2 + 1
    A = abs(A)  # Take absolute value (Shoelace can give negative area depending on orientation)
    print(int(A+1+Nedge/2))

# Part 1: Use literal direction and distance from input
def part1():
    # Arbitrary start point (coordinate system doesn't matter, only relative positions)
    pos = (0, 0)
    corners = [] 
    corners.append(pos)
    
    # Calculate and store the visited corners
    for dig in plan:
        dir, num, color = dig  # Extract: direction letter, distance, color code
        num = int(num) 
        
        # Move from current position by (direction * distance)
        pos = (pos[0] + dirs1[dir][0] * num, pos[1] + dirs1[dir][1] * num)
        corners.append(pos)
    
    # Calculate the result using Shoelace + Pick's theorem
    CalculateNtot(corners)

part1()

# Part 2: Extract direction and distance from hex color code
def part2():
    # Arbitrary start point
    pos = (0, 0)
    corners = [] 
    corners.append(pos)
    
    # Calculate and store the visited corners
    for dig in plan:
        _, _, color = dig  # Only need color: '(#70c710)'
        
        # Parse hex color: (#XXXXXY) where XXXXX = distance (hex), Y = direction
        num = int(color[2:-2], 16)  # Extract middle 5 chars, convert hex to decimal
        dir = color[-2]              # Extract second-to-last char (direction digit)
        
        # Move from current position
        pos = (pos[0] + dirs2[dir][0] * num, pos[1] + dirs2[dir][1] * num)
        corners.append(pos)
    
    # Calculate the result
    CalculateNtot(corners)

part2()
