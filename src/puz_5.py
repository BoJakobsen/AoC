#with open('testdata/5_testdata.dat') as f:
with open('data/5_data.dat') as f:
    lines=[x.strip() for x in f]

#seeds=list(map(int,(lines[0].split(':')).split()))
seeds=list(map(int,(lines[0].split())[1:]))
lines=lines[2:] #remove first lines

# structure data in dict
data={}
tabel=[]
ended=False
for line in lines:
    if not line : # we have ended
        ended = True
        data[key]=tabel
        tabel=[]
    elif not line[0].isnumeric(): # we are in the name
        key=(line.split())[0]
    else :
        tabel.append(list(map(int,line.split())))
#store the last part
data[key]=tabel

def remap(src_num,data,key):
    found=False
    for map in data[key] :
        if src_num in range(map[1],map[1]+map[2]):
            dest_num = map[0]-map[1] + src_num
            found=True
    if not found : 
        dest_num = src_num
    return dest_num
        

def full_remap(src_num,data):
    for idx in data: 
        src_num=remap(src_num,data,idx)
    return src_num

# problem 1
locations=[]
for seed in seeds :
    locations.append(full_remap(seed,data))

print(min(locations))
minloc=min(locations)

#Problem 2
locations=[]
for kk in range(int(len(seeds)/2)) :
    print(kk)
    allseeds=range(seeds[kk*2],seeds[kk*2]+seeds[kk*2+1])
    for seed in allseeds :
        loc=full_remap(seed,data)
        if loc<minloc:
            minloc=loc


print(minloc)

# did finish, but surly not the "correct solution", as it took very long to calculate : my number was: 10834440
