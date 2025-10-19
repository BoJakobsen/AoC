#  This solution was coded after seeing Neil Thistlethwaite 
#  Speed coding solution
#  I had planed to skip this one as my solution to part 1 does not in any way
#  translate to part two (and I do not really like these implementation heavy problems)
#  However seeing the solution got me to try to implement some of the ideas and
#  learn a few new things.
#  Part one used numpy and slicing this will be more plain. 

from collections import deque
import copy

ma=[]
moves=[]
with open("../data/15.dat") as f:
    for line in f:
        if line.isspace(): break
        ma.append(list(line.strip()))

    for line in f:
        moves.append(line.strip())
    moves = "".join(moves)

# change the map
ma2=[]
for l in ma:
    l2=[]
    for c in l:
        if c == '#':
            l2.append("#")
            l2.append("#")
        if c == 'O':
            l2.append("[")
            l2.append("]")
        if c == '.':
            l2.append(".")
            l2.append(".")
        if c == '@':
            l2.append("@")
            l2.append(".")
    ma2.append(l2)
ma = ma2

# find start point
for l in range(len(ma)):
    for c in range(len(ma)):
        if ma[l][c] == '@':
            pos = (l,c)


# Nice structure from Neil
dirs = {'<': (0, -1),
        '>': (0, 1),
        'v': (1,0),
        '^': (-1,0)
        }



#for l in ma:
#    print(*l)

#for move in moves:
#print(move)

for move in moves: #['v','v','v','v']:
    dir = dirs[move]


    # BFS based search thing based on the idea of Neil
    q = deque([])
    seen = set()
    q.appendleft(pos)
    seen.add(pos)
    moveit = True
    while q:
        p = q.pop()
        p_next = tupadd(p,dir)
        if ma[p_next[0]][p_next[1]] == '#':
            moveit = False
            break
        if ma[p_next[0]][p_next[1]] == ']':
            if not p_next in seen:
                q.appendleft(p_next)
                seen.add(p_next)
            if not tupadd(p_next,(0,-1)) in seen:
                q.appendleft(tupadd(p_next,(0,-1)))
                seen.add(tupadd(p_next,(0,-1)))
        if ma[p_next[0]][p_next[1]] == '[':
            if not p_next in seen:
                q.appendleft(p_next)
                seen.add(p_next)
            if not tupadd(p_next,(0,1)) in seen:
                q.appendleft(tupadd(p_next,(0,1)))
                seen.add(tupadd(p_next,(0,1)))

    if moveit: 
        #need a map copy
        new_ma = copy.deepcopy(ma)
        for p in seen:
             new_ma[p[0]][p[1]]='.'
        for p in seen:
             p_next = tupadd(p,dir)
             #print(ma[p[0]][p[1]])
             new_ma[p_next[0]][p_next[1]] = ma[p[0]][p[1]]
        ma = new_ma
        pos = tupadd(pos,dir)


#for l in ma:
#    print(*l)

res = 0
for l in range(len(ma)):
    for c in range(len(ma[0])):
        if ma[l][c]=='[':
            res += 100*l +c
print(res)
