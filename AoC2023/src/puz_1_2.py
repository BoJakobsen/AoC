nams=['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', '1' , '2', '3' ,'4', '5', '6', '7' ,'8' ,'9' ]
vals=[ 1 , 2, 3 ,4, 5, 6, 7 ,8 ,9, 1 , 2, 3 ,4 , 5, 6, 7 ,8 , 9]

with open('data/1_data.dat') as f:
    sumit=0
    for line in f:
        idx=[]
        val=[]
        idx2=[]
        val2=[]        
        for kk in range(len(nams)):
            if line.find(nams[kk])>-1:
                idx.append(line.find(nams[kk]))
                val.append(vals[kk])
            if line.rfind(nams[kk])>-1:
                idx2.append(line.rfind(nams[kk]))
                val2.append(vals[kk])
        sumit+= (val[idx.index(min(idx))]*10 + val2[idx2.index(max(idx2))])
print(sumit)


