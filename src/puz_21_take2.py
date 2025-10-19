from collections import defaultdict
import itertools
import copy
from functools import cache 



# Define positions on the numerical keyboard 
num2pos={'0': (1,0),
         'A': (2,0),
         '1': (0,1),
         '2': (1,1),
         '3': (2,1),
         '4': (0,2),
         '5': (1,2),
         '6': (2,2),
         '7': (0,3),
         '8': (1,3),
         '9': (2,3)}
num_forbitten = {(0,0)}

# define positions on the directional keyboard 
dir2pos={'<': (0,0),
         'v': (1,0),
         '>': (2,0),
         '^': (1,1),
         'A': (2,1)}

# define the movement based on the directional keyboard 
dir2move={'<': (-1,0),
         'v': (0,-1),
         '>': (1,0),
         '^': (0,1)}

# find all moves from one position to another
def unpack(ch, x, y, conv=dir2pos):
    seqs = []
    xn,yn = conv[ch]
    dx = xn - x
    dy = yn - y
    subst = ''
    if dy > 0 :
        for _ in range(abs(dy)):
            subst += '^'
    else:
        for _ in range(abs(dy)):
            subst += 'v'
    if dx > 0 :
        for _ in range(abs(dx)):
            subst += '>'
    else:
        for _ in range(abs(dx)):
            subst += '<'
    allsubst = set(list(itertools.permutations(subst)))
    for st in allsubst:
         seq = (''.join(st))
         seq += 'A'
         seqs.append(seq)
    return seqs, xn, yn


# Define all legal moves on the directional keyboard
dirkey = {}
dirs = '<>v^A'
allcombos =  list(itertools.product(dirs,repeat = 2))

for comb in allcombos:
    dirkey[comb] = []
    x0,y0 = dir2pos[comb[0]]
    seqs,_ ,_ = unpack(comb[1], x0, y0, conv=dir2pos)
    for seq in seqs:
        x = x0
        y = y0
        bad = False
        for ch in seq[:-1]:
            dx , dy = dir2move[ch]
            x += dx
            y += dy
            if x == 0 and y == 1:
                bad = True
        if not bad:
            dirkey[comb].append(seq)
 
# Define all legal moves on the numerical keyboard
numkey = {}
dirs = '0123456789A'
allcombos =  list(itertools.product(dirs,repeat = 2))

for comb in allcombos:
    numkey[comb] = []
    x0,y0 = num2pos[comb[0]]
    seqs,_ ,_ = unpack(comb[1], x0, y0, conv=num2pos)
    for seq in seqs:
        x = x0
        y = y0
        bad = False
        for ch in seq[:-1]:
            dx , dy = dir2move[ch]
            x += dx
            y += dy
            if x == 0 and y == 0:
                bad = True
        if not bad:
            numkey[comb].append(seq)

    
# test data
#codes= ['029A',
#        '980A',
#        '179A',
#        '456A',
#        '379A'
#        ]

# my data
codes = ['129A',
         '540A',
         '789A',
         '596A',
         '582A']


def expandit(keys,pad):
    res = ['']
    for kk in range(len(keys)-1):
        expands = pad[(keys[kk],keys[kk+1])]
        newres= []
        for r in res:
            for exp in expands:
                newres.append(r + exp)
        res = newres
    return res

# Inspired by Hyperneutrinos solution
# number of presses on the final keypad for moving from a to b on a given level
@cache
def npress(a,b,level):
    if level == 1:
#        print(a,b,dirkey[(a,b)])
        res = min(map(len,dirkey[(a,b)]))
    else:
        seqs = dirkey[(a,b)] # possible sequences on the next level
        res = float('inf')
        for seq in seqs:
            tem_res = 0
            for a,b in list(zip('A' + seq,  seq)):
                tem_res += npress(a,b,level - 1 )
            if tem_res < res :
                res = tem_res
    return res

# Part 1
res = 0
for code in codes:
    seqs = expandit('A'+ code, numkey) # just manually expand the first step
    minlen = float('inf')
    for seq in seqs :
        tem_res = 0
        for a,b in list(zip('A' + seq,  seq)):
            tem_res += npress(a,b,2 )
        if tem_res < minlen:
            minlen = tem_res
    res += minlen * int(code[:-1])

print(res)
    
# Part 2, is now the same, just with 25
res = 0
for code in codes:
    seqs = expandit('A'+ code, numkey) # just manually expand the first step
    minlen = float('inf')
    for seq in seqs :
        tem_res = 0
        for a,b in list(zip('A' + seq,  seq)):
            tem_res += npress(a,b,25 )
        if tem_res < minlen:
            minlen = tem_res
    res += minlen * int(code[:-1])

print(res)
    



    
