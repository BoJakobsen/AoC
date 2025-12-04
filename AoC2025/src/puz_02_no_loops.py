import math
#with open('../data/02_testdata.dat') as f:
with open('../data/02_data.dat') as f:
    rangestxt = [x.strip().split(',') for x in f]

# Convert data
ranges = []
for r in rangestxt[0]:
    ranges.append(list((r.split('-'))))


# looking at data show that we at most have the case where end has 1 mode digit than start
# This could be tested for ensure correctness, but, lets assume that ...

def find_repeat(r):
    # assumes that start and end has same number of digits
    if len(r[0]) != len(r[1]):
        return 0

    if len(r[0]) % 2 != 0:
        return 0

    rep_len = int(len(r[0])/2)

    if int(r[0][0:rep_len]) >= int(r[0][rep_len:]):
        start = int(r[0][0:rep_len])
    else:
        start = int(r[0][0:rep_len]) + 1

    if int(r[1][0:rep_len]) <= int(r[1][rep_len:]):
        end = int(r[1][0:rep_len])
    else:
        end = int(r[1][0:rep_len]) - 1

    mask = '1' + '0' * (rep_len-1) + '1'

    res = int(((int(start) + int(end))*(int(end)-int(start)+1)/2)*int(mask))
    return res


res = 0
for r in ranges:
    if len(r[0]) != len(r[1]):
        midtpoint = int('9' * len(r[0]))
        res += find_repeat([r[0], str(midtpoint)])
        res += find_repeat([str(midtpoint+1), r[1]])
    else:
        res += find_repeat(r)

print(res)


