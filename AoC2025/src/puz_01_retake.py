with open('../data/01_data.dat') as f:
    lines = [x.strip() for x in f]

# Convert L/R notation to signed rotations (L is negative, R is positive)
rots = [-int(r[1:]) if r[0] == 'L' else int(r[1:]) for r in lines]


def part1_clean():
    res = 0
    dial = 50
    for rot in rots:
        dial = (dial + rot) % 100
        if dial == 0:
            res += 1
    print('part 1: ', res)


part1_clean()


def part1_and2_clean():
    res2 = 0  # Count for part 2 (zero crossings)
    res1 = 0  # Count for part 1 (landing on zero)
    dial = 50

    for rot in rots:
        # Count full wraps (rotations beyond ±100)
        res2 += abs(rot) // 100

        newdial = (dial + rot) % 100

        # Detect single boundary crossing (wrap through 0 or 100)
        # Negative rotation wrapping to higher number
        # (handle case of start at exact 0, which should not be counted)
        # Positive rotation wrapping to lower number
        if ((rot < 0 and dial != 0 and (newdial > dial or newdial == 0))
           or (rot > 0 and newdial < dial)):
            res2 += 1

        if newdial == 0:  # handle part 1 for free
            res1 += 1

        dial = newdial

    print('part 1: ', res1)
    print('Part 2: ', res2)


part1_and2_clean()
