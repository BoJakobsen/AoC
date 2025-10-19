import copy
with open('../data/6.dat') as f:
    lines=[list(x.strip()) for x in f]

# find start
kk = 0
for line in lines:
    if '^' in line:
        a = line.index('^')
        break
    kk += 1
orgpos = (kk,a) #(line,char) positiv down

dir = (-1,0) # op

def rot(dir):
    return (dir[1],-dir[0])

def prob1(pos,dir,lin):
    lines = copy.deepcopy(lin)
    res = 0
    finished = False
    while not finished:
        if not lines[pos[0]][pos[1]] == '*':
            lines[pos[0]][pos[1]] = '*'
            res += 1
        hit = True
        while hit:
            new_pos = (pos[0]+dir[0],pos[1]+dir[1]) # if we continue
            if new_pos[0] <0 or new_pos[0] >=len(lines) or new_pos[1] <0 or new_pos[1] >=len(lines[1]):
                finished = True
                break
            if lines[new_pos[0]][new_pos[1]] == '#':
                dir = rot(dir)
            else:
                hit = False
        pos = new_pos

    return(res)

print(prob1(orgpos,dir,lines))

def prob2(orgpos,lin):
    lines = copy.deepcopy(lin)

    res = 0
    for xx in range(0,len(lines)):
        print(xx)
        for yy in range(0,len(lines[0])):
            pos = orgpos
            dir = (-1,0) # op
            if lines[xx][yy] == '.':
                lines[xx][yy] = '#'
            else:
                continue
            finished = False
            looped = False
            marks = {dir : set(), rot(dir): set(), rot(rot(dir)): set(),  rot(rot(rot(dir))):set() }
            while (not finished) and (not looped):
                if pos in marks[dir]:
                    looped = True
                    break
                marks[dir].add(pos)
                hit = True
                while hit:
                    new_pos = (pos[0]+dir[0],pos[1]+dir[1]) # if we continue
                    if new_pos[0] <0 or new_pos[0] >=len(lines) or new_pos[1] <0 or new_pos[1] >=len(lines[1]):
                        finished = True
                        break
                    if lines[new_pos[0]][new_pos[1]] == '#':
                        dir = rot(dir)
                    else:
                        hit = False
                pos = new_pos
            if looped :
                res += 1
            lines[xx][yy] = '.'
    return(res)



print(prob2(orgpos,lines))

