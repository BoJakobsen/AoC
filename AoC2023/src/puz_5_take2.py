with open('../testdata/5_testdata.dat') as f:
#with open('data/5_data.dat') as f:
    lines=[x.trip() for x in f]

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

MAXNUM=100

# dest range start, src range start, length
def unpak(data,map):
    src_start=[x[1] for x in data[map]]
    dest_start=[x[0] for x in data[map]]
    length=[x[2] for x in data[map]]
    src_end=[x+(y-1) for x,y in zip(src_start,length) ]
    dest_end=[x+(y-1) for x,y in zip(dest_start,length) ]

    new_src_start=[]
    new_src_end=[]
    new_dest_start=[]
    new_dest_end=[]
    last_end=-1
    while len(src_start)>0:
            min_src_start=min(src_start)
            min_src_start_inx=src_start.index(min_src_start)
            if min_src_start>last_end+1 : # we need a 1:1 part                
                # 1:1 part
                new_src_start.append(last_end+1)
                new_src_end.append(min_src_start-1)
                new_dest_start.append(last_end+1)
                new_dest_end.append(min_src_start-1)
                # add the smallest part
                new_src_start.append(min_src_start)
                new_src_end.append(src_end[min_src_start_inx])
                new_dest_start.append(dest_start[min_src_start_inx])
                new_dest_end.append(dest_end[min_src_start_inx])
                # update last end
                last_end=src_end[min_src_start_inx]
                #Remove used parts
                src_start.pop(min_src_start_inx)
                src_end.pop(min_src_start_inx)
                dest_end.pop(min_src_start_inx)
                dest_start.pop(min_src_start_inx)
            else: # next part is just the next
                new_src_start.append(min_src_start)
                new_src_end.append(src_end[min_src_start_inx])
                new_dest_start.append(dest_start[min_src_start_inx])
                new_dest_end.append(dest_end[min_src_start_inx])

                last_end=src_end[min_src_start_inx]
                src_start.pop(min_src_start_inx)
                src_end.pop(min_src_start_inx)
                dest_end.pop(min_src_start_inx)
                dest_start.pop(min_src_start_inx)
    if max(new_src_end)<MAXNUM: # add final part
        max_end=max(new_src_end)
        new_src_start.append(max_end+1)
        new_src_end.append(MAXNUM)
        new_dest_start.append(max_end+1)
        new_dest_end.append(MAXNUM)
    #print(new_src_start,new_src_end)
    #print(new_dest_start,new_dest_end)
    return new_src_start, new_src_end, new_dest_start, new_dest_end



def merge_maps(data,map1,map2):
    src_start1, src_end1, dest_start1, dest_end1 = unpak(data,map1)
    src_start2, src_end2, dest_start2, dest_end2 = unpak(data,map1)

    new_src_start=[]
    new_src_end=[]
    new_dest_start=[]
    new_dest_end=[]

    while len(dest_start1)>0 :
        # find src2 range of the first item
        kk=0
        while src_start2[kk] <= dest_start1[0]  :
            kk+=1
        # kk -1 should now be the index of the block 
        idx=kk-1
        #handle the two posibilities
        if dest_end1[0] <= src_end2[idx] : #the dest rang is inside
            #we can keep the src range
            new_src_start.append(src_start1[0])
            new_src_end.append(src_end1[0])
            delta=dest_start2[idx]-src_start2[idx]
            new_dest_start.append(dest_start1[0]+delta)
            new_dest_end.append(dest_end1[0]+delta)
        
            src_start1.pop(0)
            src_end1.pop(0)
            dest_start1.pop(0)
            dest_end1.pop(0)
            
        else:  # we need a split

