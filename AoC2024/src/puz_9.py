line = list(map(int,list("2333133121414131402")))

import sys
import numpy as np
sys.set_int_max_str_digits(20000)

with open('../data/9.dat') as f:
    lines = [(x.strip()) for x in f]

line = list(map(int,list(lines[0])))


## Problem 1
def prob1():

    files = line[0::2]
    spaces = line[1::2]
    Nfiles = sum(files)
    
    #disk = [None]*sum(files) # this is just for debugging
    diskidx = 0

    fillidx = len(files)-1 # inde counting from the end
    fileidx = 0 # index counting frm the begining
    spaceidx = 0

    res = 0
    while diskidx < Nfiles:
        for kk in range(files[fileidx]):
    #       disk[diskidx] = fileidx
            res += fileidx * diskidx
            diskidx += 1
        fileidx += 1
        if diskidx == Nfiles:
            break
        for kk in range(spaces[spaceidx]):
    #        disk[diskidx] = fillidx
            res += fillidx * diskidx
            files[fillidx] -= 1
            if files[fillidx] == 0:
                fillidx -= 1
            diskidx += 1
        spaceidx += 1

    print(res)


prob1()


## prob 2

def prob2():
    #array of start index of the different parts
    start_index = np.cumsum(line) - line

    files = line[0::2]
    files_index = start_index[0::2]

    spaces = np.array(line[1::2])
    spaces_index =  start_index[1::2]
    Nfiles = sum(files)


    #np.argwhere(spaces>=3)[0][0]

    #disk = [None]*sum(line) # this is just for debugging


    fill_idx = len(files)-1 # inde counting from the end
    file_idx = 0 # index counting frm the begining
    space_idx = 0

    res = 0


    for kk in range(len(files)-1,-1,-1):
        # find first space where this fits
        ind = np.argwhere(spaces>=files[kk])
        if len(ind)>0: # it can fit
            fits = False
            for aa in ind:            
                if spaces_index[aa[0]] < files_index[kk]:
                    fits = True
                    for ll in range(files[kk]):
    #                    disk[spaces_index[aa[0]]+ll] = kk
                        res += (spaces_index[aa[0]]+ll) * kk
                    spaces[aa[0]] -= files[kk]
                    spaces_index[aa[0]] += files[kk]
                    break
            if not fits:
                for ll in range(files[kk]):
     #               disk[files_index[kk]+ll] = kk
                    res += (files_index[kk]+ll) * kk

        else:
            for ll in range(files[kk]):
     #           disk[files_index[kk]+ll] = kk
                res += (files_index[kk]+ll) * kk

    print(res)

prob2()
