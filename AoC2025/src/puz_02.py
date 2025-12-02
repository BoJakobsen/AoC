import re

#single block of data
#with open('../data/02_testdata.dat') as f:
with open('../data/02_data.dat') as f:
    rangestxt = [x.strip().split(',') for x in f]

# Convert data
ranges = []
for r in rangestxt[0]:
    ranges.append(list(map(int, r.split('-'))))


def part1and2():
    res1 = 0
    res2 = 0
    pattern1 = r'^(.+)\1$'
    pattern2 = r'^(.+)\1{1,}$'
    #  ^ - start of string
    #  (.+) - capture one or more characters (this is your substring)
    #  \1 - backreference to group 1 (repeat what we just captured)
    #  one or more repetitions of \1   [for part 2] 
    #  $ - end of string
    for r in ranges:
        for num in range(r[0], r[1] + 1):
            if re.match(pattern1, str(num)):
                res1 += num
            if re.match(pattern2, str(num)):
                res2 += num
    print('part 1: ', res1)
    print('part 2: ', res2)


part1and2()
