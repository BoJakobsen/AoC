#single block of data
#with open('../data/01_testdata.dat') as f:
with open('../data/01_data.dat') as f:
    lines = [x.strip() for x in f]

rots = [-int(r[1:]) if r[0] == 'L' else int(r[1:]) for r in lines]


def part1():
    res = 0
    dial = 50
    for rot in rots:
        dial = (((dial + rot) % 100) + 100) % 100
        if dial == 0:
            res += 1
    print(res)


def part1_and2():
    res2 = 0
    res1 = 0
    dial = 50
    for rot in rots:
        fullrot = abs(rot) // 100
        res2 += fullrot
        if rot > 0:
            rot = rot - fullrot * 100
        if rot < 0:
            rot = rot + fullrot * 100
        if rot < 0 and dial != 0 and dial + rot <= 0:
            res2 += 1
        if rot > 0 and rot + dial >= 100:
            res2 += 1
        newdial = (dial + rot) % 100
        if newdial == 0:
            res1 += 1
        dial = newdial

    print('part 1: ', res1)  # part 1
    print('Part 2: ', res2)  # part 2


part1_and2()
