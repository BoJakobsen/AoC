
with open('data/2_data.dat') as f:
    sumit=0
    kk=1
    for line in f:
        possible=True
        dat1=line[0:-1].split(':')[1]
        hands=dat1.split(';')
        for hand in hands:
            collors=hand.split(',')
            for collor in collors:
                dat=collor.split(' ')
                if dat[2]=='red' and int(dat[1])>12:
                     possible=False
                if dat[2]=='green' and int(dat[1])>13:
                     possible=False
                if dat[2]=='blue' and int(dat[1])>14:
                     possible=False
        if possible:
            sumit += kk
        kk+=1
print(sumit)


