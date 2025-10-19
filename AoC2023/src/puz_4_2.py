import re

with open('data/4_data.dat') as f:
#with open('testdata/4_testdata.dat') as f:
    lines=[x.strip() for x in f]

sumit=0

# Store all cardvals in dict
cardval={}
for line in lines :
    cardnr,data_all=line.split(':')
    numwin,nummy = data_all.split('|')
    numwin =  re.findall(r'\b\d+\b', numwin)
    nummy = re.findall(r'\b\d+\b', nummy)
    cardnr = int((re.findall(r'\b\d+\b', cardnr))[0])
    n=(len(set(numwin) & set(nummy)))    
    cardval[cardnr]=n


#make dict for number of each type of cards
#initially 1
cards={(k+1):1 for k in range(len(lines))}

# update number of cards based on winning
#And sum number of cards
sumit=0
for card, ncards in cards.items() : # gives index and current number of cards
    sumit += cards[card]
    for kk in range(card+1,card+cardval[card]+1) :
        if kk<=len(cards):
            cards[kk]+=ncards

print(sumit)