import re
#
#with open('../testdata/14_testdata.dat') as f:
with open('data/14_data.dat') as f:
    lines=[x.strip() for x in f]



#def testup()



Llines=len(lines[0]) #length of a line
Nlines=len(lines) # numer of lines



def cnt_behind(lines, Nline, Nch,Ntot):
    ended= False
    k=Nline+1
    cnt=0
    while not ended:
        if  k==Nlines or lines[k][Nch] == '#' :
            ended=True
        elif lines[k][Nch] == 'O':
            cnt+=1            
        k+=1
    for kk in range(cnt):
        Ntot[Nline+1+kk]+=1
    return cnt

# empty dict for counting block per line (all we need)
Ntot={a:0 for a in range(Nlines) }

#for first line we count all
for kk in range(Llines):
    cnt=cnt_behind(lines,-1,kk,Ntot)

#for the rest count all behind # blocks
for nn in range(Nlines):
    #find all square blocks
    a= re.finditer('#',lines[nn])
    idx= [aa.start() for aa in a ]
    for kk in idx:
        cnt=cnt_behind(lines,nn,kk,Ntot)


# do the final calculation
k=Nlines
tot=0
for a in Ntot.values():
    tot+=a*k
    k-=1
print(tot)

