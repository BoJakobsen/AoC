with open('data/1_data.dat') as f:
    sumit=0
    for line in f:
        linenum=[]
        for ch in line:
            if ch.isnumeric():
                linenum.append(int(ch))
        sumit+= (linenum[0]*10 + linenum[-1])
print(sumit)


