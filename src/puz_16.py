import numpy  as np

#with open('testdata/16_testdata.dat') as f:
with open('data/16_data.dat') as f:
    lines=[x.strip() for x in f]

nplines = np.char.array([list(x) for x in lines])
nplines_shape=nplines.shape

def dirtovec(dir):
    if dir=='R':
        vec=np.array([0,1])               
    elif dir=='L':
        vec=np.array([0,-1])
    elif dir=='D' :              
        vec=np.array([1,0])
    elif dir=='U':
        vec=np.array([-1,0])
    return vec
    
def testbound(newpos):
    if newpos[0]>=nplines_shape[0] or newpos[1]>=nplines_shape[1] or newpos[0]<0 or newpos[1]<0 :
        #print(newpos)
        return True
    else: 
        return False
    
def proporgate(pos,dir):
    vec=dirtovec(dir)
    newpos=pos+vec
    if testbound(newpos):
                return
    while True:
        countit[*newpos]+=1
        while nplines[*newpos] == '.':
            newpos += vec
            if testbound(newpos):
                return 
            countit[*newpos]+=1
        if (tuple(newpos) , dir) in blist:
            return
        blist.add((tuple(newpos) , dir))
        symb=nplines[*newpos]
        if symb =='\\' and dir=='R':
            dir='D'
        elif symb =='\\' and dir=='L':
            dir='U'
        elif symb =='\\' and dir=='U':
            dir='L'
        elif symb =='\\' and dir=='D':
            dir='R'
        elif symb =='/' and dir=='R':
            dir='U'
        elif symb =='/' and dir=='L':
            dir='D'
        elif symb =='/' and dir=='U':
            dir='R'
        elif symb =='/' and dir=='D':
            dir='L'
        elif symb =='|' and (dir=='R' or dir=='L'):
            proporgate(newpos,'U')
            proporgate(newpos,'D')
            return
        elif symb =='-' and (dir=='U' or dir=='D'):
            proporgate(newpos,'R')
            proporgate(newpos,'L')
            return         
        vec=dirtovec(dir)
        newpos += vec
        if testbound(newpos):
                return 


global countit
global blist

def part1():    
    global countit
    global blist
    countit=np.zeros(nplines_shape)
    start=np.array([0,0])
    startdir='R'    
    blist=set([])
    blist.add((tuple(start) ,startdir))
    countit[*start]=1
    proporgate(start,startdir)
    print(sum(sum(countit>0)))

part1()



def traceit(start,startdir):
    global countit
    global blist
    countit=np.zeros(nplines_shape)
    blist=set([])
    blist.add((tuple(start) ,startdir))
    countit[*start]=1
    proporgate(start,startdir)
    return (sum(sum(countit>0)))

def part2():
    counts=[]
    for k in range(nplines_shape[1]) :
        x=traceit(np.array([0,k]),'D')
        counts.append(x)
    for k in range(nplines_shape[1]) :
        x=traceit(np.array([nplines_shape[0]-1,k]),'U')
        counts.append(x)
    for k in range(nplines_shape[0]) :
        x=traceit(np.array([k,0]),'R')
        counts.append(x)
    for k in range(nplines_shape[0]) :
        x=traceit(np.array([k,nplines_shape[1]-1]),'L')
        counts.append(x)
    print(max(counts))

part2()