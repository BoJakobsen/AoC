with open('../data/5.dat') as f:
    lines=[x.strip() for x in f]



# read rules into dicts
kk = 0
rules={}
while not lines[kk] == "":    
    tmp = lines[kk].split('|')
    if tmp[0] in rules:
        rules[tmp[0]].add(int(tmp[1]))
    else:
        rules[tmp[0]] = {int(tmp[1])}
    kk += 1

kk_update = kk +1 # start number for the updates

def prob1and2():
    resul1 = 0
    resul2 = 0
    for k in range(kk_update,len(lines)):
        upd = lines[k].split(',')
        upd = list(map(int,upd))
        corord = True
        for num in range(0,len(upd)-1):
            subset = set(upd[0:num+1])
            ind = str(upd[num+1])
            if ind in rules:
                if  (rules[ind] & subset):
                    corord = False
        if corord: # this is prob 1
            resul1 += (upd[int((len(upd)-1)/2)])
        else: # this is prob 2, need to find right order
            nums = set(upd)
            upd_ord = [None] * len(upd)
            for ll in range(len(upd_ord)-1,-1,-1): # build backwards               
                for num in nums: # find a number for the ll place
                    if str(num) in rules:
                        if not (rules[str(num)] & nums):
                            break
                    else:
                        break
                upd_ord[ll] = num
                nums.remove(num)
            resul2 += (upd_ord[int((len(upd_ord)-1)/2)])                        

    return(resul1, resul2)


print(prob1and2())
