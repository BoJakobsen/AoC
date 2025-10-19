### From Snippets.py

import numpy as np

# basic loader
def baseloader(filename):
    with open(filename) as f:
        lines = [(x.strip()) for x in f]
    return lines

# map is given as list of strings (or lists)
# coordinate as tuple
def checkbound(lines, coord):
    res = coord[0] >= 0 and coord[0] < len(lines) and coord[1] >= 0 and coord[1] < len(lines[0])
    return res


### Day 10


lines = baseloader('../data/10.dat')
dat = [list(map(int, list(line))) for line in lines]


def checkit(l, c):
    if dat[l][c] == 9 :
        peaks.append((l, c))
        return
    if checkbound(dat,(l-1,c)) and dat[l-1][c] == (dat[l][c] +1):
        checkit(l-1, c)
    if checkbound(dat,(l+1,c)) and dat[l+1][c] == (dat[l][c] +1):
        checkit(l+1, c)
    if checkbound(dat,(l,c-1)) and dat[l][c-1] == (dat[l][c] +1):
        checkit(l, c-1)
    if checkbound(dat,(l,c+1)) and dat[l][c+1] == (dat[l][c] +1):
        checkit(l, c+1)
    return


# problem 1 and 2 in one go
res1 = 0
res2 = 0
for ll in range(len(dat)):
    heads = np.argwhere(np.array(dat[ll])==0)
    for cc in heads:
        peaks = []
        checkit(ll,cc[0])
        res1 += len(set(peaks))
        res2 += len((peaks))

print(res1)
print(res2)

