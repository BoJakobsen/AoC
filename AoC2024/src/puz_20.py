import itertools
from collections import defaultdict


with open("../data/20.dat") as f:
    ma = [list((x.strip())) for x in f]

Nl = len(ma)
Nc = len(ma[0])

for l in range(Nl):
    for c in range(Nc):
        if ma[l][c]=='S':
            sl = l
            sc = c
        elif ma[l][c]=='E':
            el = l
            ec = c

# Map the track and time for each pint
l = sl
c = sc
cnt = 0
ch = 'S'  
track={(l,c):cnt}
while ch != 'E':
    for dl, dc in [(1, 0), (0, 1), (-1 ,0), (0,-1)]:
        if ma[l+dl][c + dc] != '#' and (l+dl , c+dc ) not in track:
            cnt += 1
            l += dl
            c += dc
            track[(l,c)]=cnt
            ch = ma[l][c] 
            break

def part1():
    # Find all cheats
    l = sl
    c = sc
    res = 0 
    ch = 'S'  
    wisited = set()
    finished = False
    while not finished:
        if (l,c) == (el, ec) : finished = True
        for dl, dc in [(1, 0), (0, 1), (-1 ,0), (0,-1)]:
            if ma[l+dl][c + dc] == '#' and (ma[(l+dl*2)%Nl][(c + dc*2)%Nc] in ['.','E']):
                saving = track[(l+dl*2,c+dc*2)] - track[(l, c)] - 2
                if saving >= 100:
#                    print((dl, dc),saving)
                    res += 1
            elif ma[l+dl][c + dc] != '#' and (l+dl , c+dc ) not in wisited:
                nl = l+ dl
                nc = c+ dc
        wisited.add((l ,c))
        l = nl
        c = nc
    print(res)

part1()

def part2():
    res = 0
    CheatMin = 100 # lest ammound we need to save
    CheatLength = 20 
    # cnt = defaultdict(int)
    for a,b in itertools.combinations(track.keys(),2):
        d =  (abs(a[0]-b[0])+abs(a[1]-b[1])) # distance of cheat
        if abs(track[a]-track[b]) - d >= CheatMin and d <= CheatLength:
            res += 1
    #        cnt[abs(track[a]-track[b]) - d] += 1   # for test data

    #for ll in cnt:
    #print(ll,cnt[ll])

    print(res)

part2()
        
#for l in ma:
#    print(*l)
