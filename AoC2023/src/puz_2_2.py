
with open('data/2_data.dat') as f:
    sumit=0
    kk=1
    for line in f:
        possible=True
        dat1=line[0:-1].split(':')[1]
        hands=dat1.split(';')
        redmax=0
        greenmax=0
        bluemax=0
        for hand in hands:
            collors=hand.split(',')            
            for collor in collors:
                dat=collor.split(' ')
                if dat[2]=='red' and int(dat[1])>redmax:
                     redmax=int(dat[1])
                if dat[2]=='green' and int(dat[1])>greenmax:
                     greenmax=int(dat[1])
                if dat[2]=='blue' and int(dat[1])>bluemax:
                     bluemax=int(dat[1])        
        sumit += redmax*bluemax*greenmax
print(sumit)
        

