from collections import defaultdict #Allows for not checking if a key exists. 

#single block of data
#with open('../testdata/22_testdata.dat') as f:
with open('../data/22_data.dat') as f:
    lines=[x.strip() for x in f]

bricks_str = [x.split('~') for x in lines]
bricks = [[list(map(int, x[0].split(','))), list(map(int, x[1].split(',')))]
          for x in bricks_str]

# sort by the smallest z value
sorted_bricks = sorted(bricks, key=lambda x: min([x[0][2], x[1][2]]))

# Dictionary for taken blocks, key is Z
block_map = defaultdict(list)  
block_map[1] = []

# Dictionary for brick block positions, key is brick number
brick_map = defaultdict(list)  

# Dictionary for brick block positions, pos is key
inv_brick_map = {}

for idx, brick in enumerate(sorted_bricks[0:]):
    if brick[0][2] == brick[1][2]:  # the brick is horizontal
        brick_blox = []
        for x in range(brick[0][0], brick[1][0]+1):
            for y in range(brick[0][1], brick[1][1]+1):
                brick_blox.append((x, y))

        fits = True  # Start at a height where it is sure to fix
        N = max(block_map.keys())+1

        # test if the brick fits
        while fits:
            if N == 0:  # handle specia case
                N = 1
                break
            for cube in brick_blox:
                if cube in block_map[N]:
                    fits = False
                    N += 1
                    break
            if fits:
                N -= 1

        # fill in the brick in the map
        block_map[N] += brick_blox
        for bb in brick_blox:
            brick_map[idx].append((bb[0], bb[1], N))
            inv_brick_map[(bb[0], bb[1], N)] = idx

    else:  # vertical brick
        xy_pos = (brick[0][0], brick[0][1])
        z_min = min([brick[0][2], brick[1][2]])
        z_max = max([brick[0][2], brick[1][2]])

        fits = True  # Start at a height where it is sure to fix
        N = max(block_map.keys())+1

        # # test if the brick fits
        while fits:
             if N == 0: #handle specia case
                 N = 1
                 break
             if xy_pos in block_map[N]:
                 fits = False
                 N += 1
                 break
             if fits:
                 N -= 1
        for bb in range(N, N + (z_max - z_min+ 1 )):
            brick_map[idx].append((xy_pos[0], xy_pos[1], bb))
            inv_brick_map[(xy_pos[0], xy_pos[1], bb)] = idx
            block_map[bb].append(xy_pos)

# The bricks are now all down
res = 0
# Find brick that can be disintegrated
for idx in range(len(sorted_bricks)):
#    print(idx)
    brick = brick_map[idx] # the brick under investigation
    above = set()
    for block in brick:
        test_block = (block[0], block[1] ,block[2]+1)
        if test_block in inv_brick_map and inv_brick_map[test_block] != idx:
            above.add(inv_brick_map[test_block])
    # test if all above blocks is supported by another brick
    cnt_safe = 0
#    print(above)
    for ab_idx in above:
        for ab_block in brick_map[ab_idx]:
            test_block = (ab_block[0], ab_block[1], ab_block[2]-1)
            if test_block in inv_brick_map and inv_brick_map[test_block] != idx and inv_brick_map[test_block] != ab_idx:
                cnt_safe += 1
                break
    if cnt_safe == len(above) or len(above) == 0:
        # it can be remove
#        print('safe')
        res += 1
print(res)
