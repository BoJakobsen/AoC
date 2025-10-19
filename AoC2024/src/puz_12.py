# Snippets.py is loaded before running this
# Load packages and defines a few help functions

# lines = baseloader('../data/12_test.dat')
lines = baseloader('../data/12.dat')

# Organise data in dict after type
dat = defaultdict(list)
for Nll, ll in enumerate(lines):
    for Ncc, cc in enumerate(ll):
        dat[cc].append((Nll,Ncc))

# get all neighbour points, within boundary
def get_nab(coord):
    dirs=[(1,0), (0,1), (-1,0), (0,-1)]
    nabs=[]
    for d in dirs:
        if checkbound(lines, tupadd(d,coord)):
            nabs.append(tupadd(d,coord))
    return nabs

# get all neighbour points, ignoring boundary
def get_nab2(coord):
    dirs=[(1,0), (0,1), (-1,0), (0,-1)]
    nabs=[]
    for d in dirs:
        nabs.append(tupadd(d,coord))
    return nabs

# Find the distinct connected regions, and organise in new structure
groups = defaultdict(list)
for kind in dat.keys():
    poss = copy.copy(dat[kind])
    while len(poss)>0:
        grp = [poss[0]]  # add first position to the group
        poss.remove(grp[0])  # remove from list
        added = True
        while added:
            added = False 
            for pos in poss:  # check if we can add a number
                nab = get_nab(pos)
                if set(nab).intersection(set(grp)):  # is nab a neighbour
                    grp.append(pos)
                    poss.remove(pos)
                    added = True
                    break
        groups[kind].append(grp)
 
# Problem 1 can now easily be calculated
res = 0
for regs in groups.values():
    for reg in regs:
        ares = len(reg)
        per = 0
        for point in reg:
            per += 4-len(set(get_nab2(point)).intersection(set(reg)))  # number of edges
        res += ares * per
print(res)

# Find square boundaries of a connected region
def minmax(reg):
    minl = len(lines)
    maxl = 0
    minc = len(lines[0])
    maxc = 0
    for p in reg:
        if p[0] < minl :
            minl = p[0]
        if p[0] > maxl :
            maxl = p[0]
        if p[1] < minc :
            minc = p[1]
        if p[1] > maxc :
            maxc = p[1]
    return minl,maxl,minc,maxc
 

# Problem 2

# For each connected region scan along vertical and horizontal lines and
# count edge, not very compact/optimised solution, but the algorithm works
res = 0
for key , regs in groups.items():
    for reg in regs:
        bound = minmax(reg) # line char
        sides = 0
        # Count horizontal edge
        for l in range(bound[0]-1,bound[1]+2):
            ingrp_down = False
            ingrp_up = False
            for c in range(bound[2],bound[3]+1):
                if not ingrp_down and (l+1,c) in reg and (l,c) not in reg: 
                    ingrp_down = True
                    sides += 1
                if ingrp_down and ((l+1,c) not in reg or (l,c)  in reg): 
                    ingrp_down = False
                if not ingrp_up and (l-1,c) in reg and (l,c) not in reg: 
                    ingrp_up = True
                    sides += 1
                if ingrp_up and ((l-1,c) not in reg or (l,c)  in reg): 
                    ingrp_up = False

        # Count vertical edge
        for c in range(bound[2]-1,bound[3]+2):
            ingrp_left = False
            ingrp_right = False
            for l in range(bound[0],bound[1]+1):
                if not ingrp_right and (l,c+1) in reg and (l,c) not in reg: 
                    ingrp_right = True
                    sides += 1
                if ingrp_right and ((l,c+1) not in reg or (l,c)  in reg): 
                    ingrp_right = False
                if not ingrp_left and (l,c-1) in reg and (l,c) not in reg: 
                    ingrp_left = True
                    sides += 1
                if ingrp_left and ((l,c-1) not in reg or (l,c)  in reg): # end of grp
                    ingrp_left = False
        res += sides * len(reg)
print(res)
