from collections import deque

with open("../data/18.dat") as f:
    data = [tuple(map(int,((x.strip()).split(',')))) for x in f]

size = 70

Nbytes= 2024
grid = [[0] * (size + 1) for _ in range(size + 1)]


for n in range(Nbytes):
    c, r = data[n]
    grid[r][c] = 1

    
# start
sr = 0
sc = 0
# end
er = size
ec = size


for kk in range(2024,3024):
    c,r = data[kk]
    grid[r][c] = 1


    q = deque([(sr , sc, 0)])
    seen = {(sr , sc)}

    solved = False
    while q and not solved:
        r, c ,d = q.popleft() 
        for nr, nc in [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]:
            if nr < 0 or nr > size or nc < 0 or nc > size: continue
            if grid[nr][nc] == 1 : continue
            if (nr, nc) in seen: continue
            if nr == er and nc == ec :
                print(d+1)
                solved = True
            seen.add((nr, nc))
            q.append((nr, nc, d+1))
    if not solved:
        print(data[kk])
        break

#for r in range(maxr):
#    for c in range(maxc):
#        if (r,c) in data[:Nbytes]:
#            print('#',end= '' )
#        else:
#            print('.', end = '')
#    print('')
