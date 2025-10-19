# Day 11, Problem 1 and 2

# advance 25 blinks and return the new list
def advance(dat):
    dat = [dat]
    for aa in range(0,25):
        newdat =[]
        for kk in range(len(dat)):
            num = dat[kk]
            if num == 0:
                newdat.append(1)
            elif len(str(num)) % 2 == 0:
                strnum = str(num)
                newdat.append(int(strnum[0:int(len(strnum)/2)]))
                newdat.append(int(strnum[int(len(strnum)/2):]))
            else:
                newdat.append(num * 2024)
        dat = copy.copy(newdat)
    return dat



line = '41078 18 7 0 4785508 535256 8154 447'
dat0 = list(map(int,(line.split())))

# Do 3 x 25 blinks, record results after each.
dict = {}
dat1 = copy.copy(dat0)
for aa in range(3):
    dat =  list(set(dat1))
    dat1=[]
    for kk in dat:
        dat2 = advance(kk)
        unique2 = list(set(dat2))
        unique2.sort()
        cnt2=[]
        for n in unique2:
            cnt2.append(dat2.count(n))
        dict[kk] = (unique2, cnt2)
        dat1 += unique2

# Problem 1
res = 0
for aa in dat0:
    a,b = dict[aa]
    print(sum(b))
    print(a)
    res += sum(b)
print(res)

# Calculate result of part 2
res = 0
for kk in dat0:
    unique, cnt = dict[kk]
    for jj,Njj in zip(unique,cnt):
        unique1, cnt1 = dict[jj]
        for ll,Nll in zip(unique1,cnt1):
            unique2, cnt2 = dict[ll]
            res += sum(cnt2)*Nll*Njj
print(res)
