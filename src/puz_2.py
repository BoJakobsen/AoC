import numpy as np

with open('../data/2.dat') as f:
    lines=[x.strip() for x in f]

def prob1():
    n_safe=0
    for line in lines:
        a = np.array(list(map(int,line.split())))
        a_inc = np.sort(a)
        a_dec = a_inc[::-1]
        if (a == a_dec).all() or (a == a_inc).all():
            d = np.abs(a[1:] -  a[0:-1])
            if (d>0).all() and (d<=3).all():
                n_safe += 1
    return n_safe

print(prob1())


def testit(a):
    a_inc = np.sort(a)
    a_dec = a_inc[::-1]
    if (a == a_dec).all() or (a == a_inc).all():
        d = np.abs(a[1:] -  a[0:-1])
        if (d>0).all() and (d<=3).all():
            return True

def prob2():
    n_safe=0
    for line in lines:
        a = np.array(list(map(int,line.split())))
        if testit(a):
            n_safe += 1
        else:
            fixed = False
            for k in range(len(a)):
                if testit(np.delete(a,k)) :
                    fixed = True
            if fixed :
                n_safe += 1
    return n_safe

print(prob2())
