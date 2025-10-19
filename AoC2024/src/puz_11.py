import copy
from collections import deque


#line = '125 17' # test data
line = '41078 18 7 0 4785508 535256 8154 447'
dat = list(map(int,(line.split())))

def prob1(dat):
    for aa in range(0,25):
        print(aa)
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
    print(len(dat))

 prob1(dat)


# try with a que
def prob1_que(dat):
    res = 0
    Nmax = 24 # blinks -1
    q = deque([])
    for aa in dat:
        q.append((aa, Nmax))
    while len(q) > 0:
        num,rang = q.pop()
        if rang == 0: # we are at the bottom
            if num == 0:
                res += 1
            elif len(str(num)) % 2 == 0:
                res += 2
            else:
                res += 1
        else: #need to handle children    
            if num == 0:
                q.append((1, rang-1))
            elif len(str(num)) % 2 == 0:
                strnum = str(num)
                q.append(((int(strnum[0:int(len(strnum)/2)])), rang-1))
                q.append(((int(strnum[int(len(strnum)/2):])), rang-1))
            else:
                q.append((num * 2024, rang -1))
    print(res)
    # Fast but still not enough.

prob1_que(dat)
