from collections import defaultdict  # Allows for not checking if a key exists

# Extensive commented by claude.ai

# Day 22: Falling sand bricks simulation
# Goal: Drop bricks vertically until they settle, then find which can be safely removed

# Read and parse input
#with open('../testdata/22_testdata.dat') as f:
with open('../data/22_data.dat') as f:
    lines = [x.strip() for x in f]

# Parse brick coordinates from "x1,y1,z1~x2,y2,z2" format
bricks_str = [x.split('~') for x in lines]
bricks = [[list(map(int, x[0].split(','))), list(map(int, x[1].split(',')))]
          for x in bricks_str]
# Result: bricks = [[[x1,y1,z1], [x2,y2,z2]], ...]

# Sort bricks by minimum z-coordinate (bottom-most first)
# This ensures we drop bricks in the correct order (lowest first)
sorted_bricks = sorted(bricks, key=lambda x: min([x[0][2], x[1][2]]))

# Data structures for tracking brick positions:
# block_map: For each z-level, which (x,y) positions are occupied
# Key: z-coordinate, Value: list of (x,y) tuples at that height
block_map = defaultdict(list)  
block_map[1] = []  # Ground level (z=1) starts empty

# brick_map: For each brick, what positions does it occupy
# Key: brick index, Value: list of (x,y,z) tuples
brick_map = defaultdict(list)  

# inv_brick_map: For each position, which brick occupies it
# Key: (x,y,z) tuple, Value: brick index
inv_brick_map = {}

# ============================================================================
# PHASE 1: Drop all bricks to their resting positions
# ============================================================================

for idx, brick in enumerate(sorted_bricks):
    # Check if brick is horizontal (same z-coordinate for both ends)
    if brick[0][2] == brick[1][2]:
        # Horizontal brick - can span multiple x,y positions at same z
        
        # Generate all (x,y) positions this brick occupies
        brick_blox = []
        for x in range(brick[0][0], brick[1][0] + 1):
            for y in range(brick[0][1], brick[1][1] + 1):
                brick_blox.append((x, y))
        
        # Find lowest z where this brick can rest
        fits = True
        N = max(block_map.keys()) + 1  # Start above all existing bricks
        
        # Test each z-level going downward
        while fits:
            if N == 0:  # Can't go below ground (z=1)
                N = 1
                break
            
            # Check if any block position is already occupied at level N
            for cube in brick_blox:
                if cube in block_map[N]:
                    fits = False  # Collision detected
                    N += 1  # Use the level above
                    break
            
            if fits:
                N -= 1  # Try one level lower
        
        # Place brick at level N
        block_map[N] += brick_blox  # Mark (x,y) positions as occupied at this z
        for bb in brick_blox:
            brick_map[idx].append((bb[0], bb[1], N))  # Record brick position
            inv_brick_map[(bb[0], bb[1], N)] = idx  # Record reverse mapping
    
    else:
        # Vertical brick - single (x,y) position, multiple z levels
        
        xy_pos = (brick[0][0], brick[0][1])  # x,y position (same for all blocks)
        z_min = min([brick[0][2], brick[1][2]])
        z_max = max([brick[0][2], brick[1][2]])
        
        # Find lowest z where bottom of brick can rest
        fits = True
        N = max(block_map.keys()) + 1
        
        while fits:
            if N == 0:
                N = 1
                break
            
            # Check if (x,y) position is occupied at level N
            if xy_pos in block_map[N]:
                fits = False
                N += 1
                break
            
            if fits:
                N -= 1
        
        # Place vertical brick from level N to N + height
        brick_height = z_max - z_min + 1
        for bb in range(N, N + brick_height):
            brick_map[idx].append((xy_pos[0], xy_pos[1], bb))
            inv_brick_map[(xy_pos[0], xy_pos[1], bb)] = idx
            block_map[bb].append(xy_pos)

# ============================================================================
# PHASE 2: Find which bricks can be safely disintegrated
# ============================================================================

# A brick can be removed if all bricks above it are supported by other bricks

res = 0  # Count of safe-to-remove bricks

for idx in range(len(sorted_bricks)):
    brick = brick_map[idx]  # Get all blocks of this brick
    
    # Find all bricks directly above this one
    above = set()
    for block in brick:
        # Check position one level above each block
        test_block = (block[0], block[1], block[2] + 1)
        if test_block in inv_brick_map and inv_brick_map[test_block] != idx:
            above.add(inv_brick_map[test_block])  # Different brick found above
    
    # For each brick above, check if it has alternative support
    cnt_safe = 0
    for ab_idx in above:
        # Check all blocks of the brick above
        for ab_block in brick_map[ab_idx]:
            # Look one level below
            test_block = (ab_block[0], ab_block[1], ab_block[2] - 1)
            
            # If there's a different brick below (not current, not itself)
            if (test_block in inv_brick_map and 
                inv_brick_map[test_block] != idx and 
                inv_brick_map[test_block] != ab_idx):
                cnt_safe += 1  # This brick above has alternative support
                break
    
    # Safe to remove if all bricks above have alternative support
    if cnt_safe == len(above) or len(above) == 0:
        res += 1

print(res)
