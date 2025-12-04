#with open('../data/04_testdata.dat') as f:
with open('../data/04_data.dat') as f:
    grid = [x.strip() for x in f]

Nl = len(map)  # Number of lines
Nc = len(map[0])  # Number of columns

# All 8 directions: right, down, left, up, and 4 diagonals
adjs = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]


def part1():
    res = 0
    for l in range(Nl):
        for c in range(Nc): 
            if grid[l][c] == '.':
                #print('.', end="")
                continue
            Nrol = 0
            for adj in adjs:
                dl, dc = adj
                test_l, test_c = (l + dl, c + dc)
                if test_l not in range(Nl) or test_c not in range(Nc):
                    continue
                if grid[test_l][test_c] == '@':
                    Nrol += 1
            if Nrol < 4:
                #print('#', end="")
                res += 1
            else:
                pass
                #print('@', end="")
        #print('')
    print("Part 1: ", res)

part1()

# #######################
# Part 2 (with part 1 as sub-set)
# #######################


def grid_to_set(grid):
    """Extract positions of all '@' characters into a set."""
    rolls = set()
    for l in range(Nl):
        for c in range(Nc):
            if grid[l][c] == '@':
                rolls.add((l, c))
    return rolls


def find_removable(rolls):
    """Find all positions with fewer than 4 neighbors.

    Returns: (count of removable, set of removable positions)
    """
    res = 0
    removable = set()

    for pos in rolls:
        l, c = pos
        Nrol = 0  # Count neighbors

        # Check all 8 adjacent positions
        for adj in adjs:
            dl, dc = adj
            test_l, test_c = (l + dl, c + dc)
            
            # Skip if out of bounds
            if test_l not in range(Nl) or test_c not in range(Nc):
                continue
            
            # Count if neighbor exists
            if (test_l, test_c) in rolls:
                Nrol += 1
            
            # Early exit - already has 4+ neighbors
            if Nrol >= 4:
                break
        
        # Mark for removal if fewer than 4 neighbors
        if Nrol < 4:
            removable.add((l, c))
            res += 1
    
    return res, removable


def part1_and_2():
    rolls = grid_to_set(grid)
    
    # Part 1: Initial removable count
    res, removable = find_removable(rolls)
    print("Part 1: ", res)
    
    # Part 2: Iteratively remove until stable
    while len(removable) > 0:
        rolls = rolls - removable
        res_sub, removable = find_removable(rolls)
        res += res_sub
    
    print("Part 2: ", res)


part1_and_2()
