import re
import numpy as np

with open('../data/4.dat') as f:
    lines=[x.strip() for x in f]


# regex solution using 90 deg rotations
def prob1(lines):
    Nres = 0
    for rot in range(0,4):
        # rotate
        lines = list(zip(*lines[::-1]))

        # count in lines 
        for line in lines:
            res = re.findall("XMAS","".join(line))         
            Nres += len(res)

        # upper half diagonals
        for kk in range(0,len(lines)):
            diag=""
            rr = kk+1
            for ll in range(0,kk+1) :
                rr -= 1
                diag += lines[ll][rr]
            res = re.findall("XMAS",diag)         
            Nres += len(res)

        # Lower half diagonals 
        for kk in range(1,len(lines)):
            diag=""
            rr = len(lines)
            for ll in range(kk,len(lines)):    
                rr -= 1
                diag += lines[ll][rr]
            res = re.findall("XMAS",diag)         
            Nres += len(res)

    return Nres

# very basic solution her, works fine on these size of puzzle
def prob2(lines):
    Nres = 0
    for ll in range(1,len(lines)-1):
        for rr in range(1,len(lines)-1):
            if lines[ll][rr] == "A":
                d1 = lines[ll-1][rr-1] + lines[ll][rr] + lines[ll+1][rr+1]
                d2 = lines[ll-1][rr+1] + lines[ll][rr] + lines[ll+1][rr-1]
                if (d1 == "SAM" or d1 == "MAS") and (d2 == "SAM" or d2 == "MAS"):
                    Nres +=1
    return Nres


print(prob1(lines))
print(prob2(lines))
