import itertools as it
#
#with open('../testdata/12_1_testdata.dat') as f:
with open('data/12_data.dat') as f:
    lines=[x.strip() for x in f]


# Split the data into the twp parts
records=[]
contgrp=[]
for line in lines:
    tmp=line.split()
    records.append(tmp[0])
    contgrp.append(list(map(int,tmp[1].split(','))))


def checkit(rec,contgrp,fill):
    ingrp=False
    cnt=0
    k=0
    contgrp_test=[]
    for ch in rec:
        if ch == '?':
            ch=fill[k]
            k+=1
        if ch == '#' and not ingrp:
            ingrp=True
            cnt+=1
        elif ch =='#' and ingrp:
            cnt+=1
        elif ch =='.' and ingrp:
            ingrp=False
            contgrp_test.append(cnt)
            cnt=0
    if ingrp : # handle end case
            contgrp_test.append(cnt)
    if contgrp == contgrp_test:
        res= True
    else :
        res=False
    return res

def countit():
    total=0
    for kk in range(len(records)):
        print(kk)
        cnt=0
        Nmissing=records[kk].count('?')
        fills=it.product('.#',repeat=Nmissing)
        for fill in fills: 
            if checkit(records[kk],contgrp[kk],fill):            
                cnt+=1
        total += cnt
    print(total)

#Problem 1
countit()
