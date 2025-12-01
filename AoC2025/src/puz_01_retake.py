#with open('../data/01_testdata.dat') as f:
with open('../data/01_data.dat') as f:
    lines = [x.strip() for x in f]

rots = [-int(r[1:]) if r[0] == 'L' else int(r[1:]) for r in lines]

# Cleaned up version with more clear logic


# Clean part 1 implementation
def part1_clean():
    res = 0
    dial = 50
    for rot in rots:
        dial = ((dial + rot) % 100)
        if dial == 0:
            res += 1
    print('part 1: ', res)  # part 1


part1_clean()


def part1_and2_clean():
    res2 = 0
    res1 = 0
    dial = 50
    for rot in rots:
        res2 += abs(rot) // 100
        newdial = (dial + rot) % 100
        if ((rot < 0 and dial != 0 and (newdial > dial or newdial== 0))
           or (rot > 0 and newdial < dial)):
            res2 += 1
        if newdial == 0:
            res1 += 1
        dial = newdial

    print('part 1: ', res1)  # part 1
    print('Part 2: ', res2)  # part 2


part1_and2_clean()
