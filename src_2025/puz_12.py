import itertools as it
from functools import cache


#
#with open('../testdata/12_1_testdata.dat') as f:
with open('../data/12_data.dat') as f:
    lines=[x.strip() for x in f]


# Split the data into the two parts
rec=[]
cgrp=[]
for line in lines:
    tmp=line.split()
    rec.append(tmp[0])
    cgrp.append(list(map(int,tmp[1].split(','))))

# Checkit after filling in right number of '.'
def checkit(rec,cgrp):
    ingrp = False
    cnt = 0
    contgrp_test = []
    for ch in rec:
        if (ch == '#' or ch == '?') and not ingrp:
            ingrp = True
            cnt += 1
        elif (ch == '#' or ch == '?') and ingrp:
            cnt += 1
        elif ch =='.' and ingrp:
            ingrp = False
            contgrp_test.append(cnt)
            cnt = 0
    if ingrp :  # handle end case
            contgrp_test.append(cnt)
    if cgrp == contgrp_test:
        res = True
    else:
        res = False
    return res


#  Optimized a bit compared to old solution
#  still be to slow

def prob1() :
    res = 0
    for Nres in range(0,len(rec)):

        # Lets find all numbers we can
        N = len(rec[Nres]) # total springs
        Ndam = sum(cgrp[Nres]) # total damaged springs
        Nop = N-Ndam # Total operational springs

        Nunk = rec[Nres].count('?') # number of unknown springs
        Nop_seen = rec[Nres].count('.') # seen operational springs
        Ndam_seen = rec[Nres].count('#') # seen operational springs

        Nop_toplace = Nop - Nop_seen
        Ndam_toplace = Ndam - Ndam_seen

        IDXunk = [i for i, ltr in enumerate(rec[Nres]) if ltr == '?'] # index for unknowns

        # all ways to place the operational springs
        permut = list(it.combinations(range(Nunk),Nop_toplace))

        for jj in permut:
            Trec = list(rec[Nres])
            for kk in jj:
                Trec[IDXunk[kk]] = '.'
                # all operational is now in, so left over ? is broken
            if checkit(Trec,cgrp[Nres]):
                res += 1

    print(res)


prob1()


def prob2_slow():
    # Way to slow, permutations explodes
    # Works on the small ones on the tests but no chance on the larger ones. 
    res = 0
    for Nres in [1]:  # range(0,len(rec)):
        rec2 = rec[Nres] + '?' + rec[Nres] + '?' + rec[Nres] + '?' + rec[Nres] + '?' + rec[Nres] 
        cgrp2 = cgrp[Nres]*5

        # Lets find all numbers we can
        N = len(rec2)  # total springs
        Ndam = sum(cgrp2)  # total damaged springs
        Nop = N-Ndam  # Total operational springs

        Nunk = rec2.count('?')  # number of unknown springs
        Nop_seen = rec2.count('.')  # seen operational springs
        Ndam_seen = rec2.count('#')  # seen operational springs

        Nop_toplace = Nop - Nop_seen
        Ndam_toplace = Ndam - Ndam_seen

        IDXunk = [i for i, ltr in enumerate(rec2) if ltr == '?']  # index for unknowns

        # all ways to place the operational springs
        permut = (it.combinations(range(Nunk),Nop_toplace))

        for jj in permut:
            Trec = list(rec2)
            for kk in jj:
                Trec[IDXunk[kk]] = '.'
                # all operational is now in, so left over ? is broken springs
            if checkit(Trec,cgrp2):
                res += 1
                print(res)
    print(res)
# prob2_slow()


# partly recursive solution
def checkit2(rec, cgrp, ingrp):
    global count, callcnt
    #  print(rec, cgrp, ingrp)
    for idx, ch in enumerate(rec):
        #  print(ch, ingrp,cgrp)
        if ch == '?':
            rec[idx] = '#'
            checkit2(rec[idx:].copy(), cgrp.copy(), ingrp)
            rec[idx] = '.'
            checkit2(rec[idx:].copy(), cgrp.copy(), ingrp)
            return True
        elif (ch == '#') and not ingrp:
            if len(cgrp) > 0:
                ingrp = True
                cgrp[0] -= 1
            else:
                return False
        elif (ch == '#') and ingrp:
            if len(cgrp) > 0 and cgrp[0] >= 1:
                cgrp[0] -=1
            else:
                return False
        elif ch == '.' and ingrp:
            if cgrp[0] == 0:
                cgrp = cgrp[1:]
                ingrp = False
            else:
                return False
    if len(cgrp) == 0 or (len(cgrp) == 1 and cgrp[0] == 0):
        count = count + 1
        print('OK')
        return True
    else:
        return False


# This works, but is still to slow
count = 0


def prob2_recursive_slow():
    global count
    for Nres in range(0, len(rec)):
        print(Nres)
        rec2 = rec[Nres] #+ '?' + rec[Nres] + '?' + rec[Nres] + '?' + rec[Nres] + '?' + rec[Nres] 
        cgrp2 = cgrp[Nres]#*5
        checkit2(list(rec2), cgrp2, False)
    print(count)


#prob2_recursive_slow()


# optimized for use of cache, all input needs to be immutable, and no global variables
# Not the prettiest code, states could be more clearly defined.
@cache
def checkit3(rec, rec_index0, cgrp, cgrp_index0, cur_cgrp0):
    count = 0
    ch0 = rec[rec_index0]
    ch = ''
    finished = False
    while not finished:
        rec_index = rec_index0
        cgrp_index = cgrp_index0
        cur_cgrp = cur_cgrp0
        if ch0 != '?':
            ch = ch0
            finished = True
        else:
            if ch == '':
                ch = '#'
            else:
                ch = '.'
                finished = True
        if (ch == '#') and cur_cgrp == 0:  # start of new group 
            if (cgrp_index < len(cgrp)) and cgrp[cgrp_index] > 0:
                cur_cgrp = 1
            else:
                continue
        elif (ch == '#') and cur_cgrp > 0:  # in a group
            if cgrp[cgrp_index] > cur_cgrp:
                cur_cgrp += 1
            else:
                continue
        elif ch == '.' and cur_cgrp > 0:  # leaving a group
            if (cur_cgrp == cgrp[cgrp_index]):
                cgrp_index += 1
                cur_cgrp = 0
            else:
                continue
        if (rec_index == len(rec)-1):  # we are at the end
            if cur_cgrp == 0:  # we are not in a groupe
                if cgrp_index != len(cgrp):   # we have index past last element
                    continue
            else:  # we are in a group
                if (cgrp[cgrp_index] != cur_cgrp) or (cgrp_index != len(cgrp)-1):
                    continue
            count += 1
        else:
            rec_index += 1
            count += checkit3(rec, rec_index, cgrp, cgrp_index, cur_cgrp)
    return count


def prob2_recursive_optimized():
    tot = 0
    for Nres in range(0, len(rec)):
        rec2 = rec[Nres] + '?' + rec[Nres] + '?' + rec[Nres] + '?' + rec[Nres] + '?' + rec[Nres] 
        cgrp2 = cgrp[Nres]*5
        tot += checkit3(rec2, 0, tuple(cgrp2), 0, 0)
    print(tot)


prob2_recursive_optimized()
