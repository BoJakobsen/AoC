import itertools
import copy
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


def expand(code,conv):
    seqs = ['']
    ch0 = 'A'
    for ch in code:
        newseqs = conv[(ch0,ch)]
        tmp = []
        for nseq in newseqs:
            for seq in seqs:
              tmp.append(seq + nseq)
        seqs = tmp
        ch0 = ch
    return seqs

# For the last part we, only need the numer of presses, not the actual sequences,
# much faster 
def expand3(code,conv=dirkey):
    seqlen = 0
    ch0 = 'A'
    for ch in code:
        newseqs = conv[(ch0,ch)]
        seqlen += len(newseqs[0]) 
        ch0 = ch
    return seqlen

    
# test data
# codes= ['029A',
#         '980A',
#         '179A',
#         '456A',
#         '379A' ]

# my data
codes = ['129A',
        '540A',
        '789A',
        '596A',
        '582A']

# Part 1
res = 0
for code in codes:

    # 1 conversion
    seq1s = expand(code,numkey)

    # 2 convertsion
    tmp = []
    for seq in seq1s:
        seq2s = expand(seq,dirkey)
        tmp += seq2s
    minval = min(list(map(len,tmp)))
    res2s = [tmp[kk]  for kk in range(len(tmp)) if len(tmp[kk])== minval ]

    # 3 convertsion
    minval = float("inf")
    for seq in res2s:
        len3exp = expand3(seq)
        if len3exp < minval :
            minval = len3exp

    print(code)
    print(minval)
    res += int(code[:3]) * minval

print(res)

