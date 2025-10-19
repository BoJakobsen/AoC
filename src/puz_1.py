from copy import deepcopy
import numpy as np

with open('../data/1.dat') as f:
    lines=[x.strip() for x in f]


x1 = np.array([])
x2 =  np.array([])
for line in lines:
    a1 , a2 = line.split()
    x1 = np.append(x1,int(a1))
    x2 = np.append(x2,int(a2))


def prob1():    
    d = np.sort(x1)-np.sort(x2)
    return np.sum(np.abs(d))


def prob2():
    res = 0
    for x in x1:
        res = res + np.sum(x2 == x) * x
    return res

print(prob1())

print(prob2())
