import re

with open('data/4_data.dat') as f:
#with open('testdata/4_testdata.dat') as f:
    lines=[x.strip() for x in f]

sumit=0

for line in lines :
    _,data_all=line.split(':')
    numwin,nummy = data_all.split('|')
    numwin =  re.findall(r'\b\d+\b', numwin)
    nummy = re.findall(r'\b\d+\b', nummy)
    #print(numwin,nummy)
    n=(len(set(numwin) & set(nummy)))    
    if n>0 :
        print(set(numwin) & set(nummy), n, 2**(n-1))
        sumit += 2**(n-1)
    else: 
        print(0 , 0)
print(sumit)