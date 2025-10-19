import numpy as np

map_l=[]
moves=[]
with open("../data/15.dat") as f:
    for line in f:
        if line.isspace(): break
        map_l.append(list(line.strip()))
        if '@' in line:
            pos = (len(map_l)-1, line.index('@'))
    ma  = np.array(map_l)

    for line in f:
        moves.append(line.strip())
    moves = "".join(moves)


for mov in moves:
 #   print(ma)
 #   print(mov)
    if mov == '>':
        #move right
        part = ma[pos[0],pos[1]:]
        mdir = (0,1)
    elif mov == '<':
        #move left
        part = ma[pos[0],pos[1]::-1]
        mdir = (0,-1)
    elif mov == 'v':
        #move down
        part = ma[pos[0]:,pos[1]]
        mdir = (1,0)
    elif mov == '^':
        #move up
        part = ma[pos[0]::-1,pos[1]]
        mdir = (-1,0)

    # with this slicing all cases are now the same
    if part[1] == '.' : #next is free
        part[0] = '.'
        part[1] = '@'
        pos = tupadd(pos,mdir)
    elif part[1] == 'O' : #next is a box
        indx = np.where(part=='.')
        indx_wall = np.where(part=='#')
        if len(indx[0])>0  and indx[0][0]  < indx_wall[0][0]:
            part[1:indx[0][0]+1] = part[:indx[0][0]]
            part[0] = '.'
            pos = tupadd(pos,mdir)
    # only alternative is a wall and we do not move then
 #   print(ma)
 #   input("ak")


# Calculate sum of GPS coordinates
res = 0
for nl,li in enumerate(ma):
    boxs = np.where(li == 'O')
    res += np.sum(boxs[0]) + len(boxs[0])*nl*100
print(res)
