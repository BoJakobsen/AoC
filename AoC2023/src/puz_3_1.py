

def cc(x):
    if (not x.isnumeric()) and (not x=='.'):
        isgood = True
    else :
        isgood =False
    return isgood

def ccl(x): #On the line
    if  (not x=='.') and (not x.isnumeric()):
        isgood = True
    else :
        isgood =False
    return isgood


file = open('data/3_data.dat', 'r')
lines = file.readlines()
file.close()

nums=[]
isgoods=[]

for index, line in enumerate(lines): #loop the lines
    #print("Line {}: {}".format(index, line.strip()))
    innum=False
    isgood=False
    numstr=''
    for chindex, ch in enumerate(line.strip()) :
        if  ch.isnumeric() : #we are in a number
            numstr += ch
            innum = True

            # check all the nab, not very nice solution
            # Just check the 6 nabs 
            if index>0 and chindex>0 :
                if cc(lines[index-1][chindex-1]) :
                    isgood = True
            
            if index>0  :
                if cc(lines[index-1][chindex]):
                    isgood = True
            
            if index>0 and (chindex< (len(line.strip())-2) ):
                if cc(lines[index-1][chindex+1])  :
                    isgood = True

            if chindex>0 :
                 if ccl(lines[index][chindex-1]) : 
                    isgood = True

            if chindex>0 and (chindex< (len(line.strip())-2)):
                 if ccl(lines[index][chindex+1]) :
                    isgood = True

            if index<len(lines)-2 and chindex>0 :
                if cc(lines[index+1][chindex-1]) :
                    isgood = True
            
            if index<len(lines)-2 :
                if cc(lines[index+1][chindex]):
                    isgood = True
            
            if index<len(lines)-2 and (chindex< (len(line.strip())-2) ):
                if cc(lines[index+1][chindex+1])  :
                    isgood = True


        elif (not ch.isnumeric()) and innum  : # a number has ended
            innum = False
            nums.append(int(numstr))
            isgoods.append(isgood)
            numstr=''
            isgood=False
    if innum : # line has ended and we are in a number
            nums.append(int(numstr))
            isgoods.append(isgood)




print(nums)
print(isgoods)

sumit=0

for idx, val in enumerate(nums) : 
    if isgoods[idx] :
        sumit += val

print(sumit)


    
