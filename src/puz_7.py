import itertools

with open('../data/7.dat') as f:
    lines=[(x.strip()).split(':') for x in f]

# split input to lists
testvals = [int(line[0])  for line in lines]
eqs = [list(map(int,line[1].split()))  for line in lines]


def calc(eqs,Ops):
    res = eqs[0]
    for eq,op in zip(eqs[1:],Ops):
        res = eval(str(res) + op + str(eq))
    return(res)

# a bit slow solution, looping too much, but ok works
def prob1():
    res = 0
    Nres = 0
    for val,eq in zip(testvals,eqs):
        Nop = len(eq)-1
        Ops = list(itertools.product('+*',repeat=Nop))
        for op in Ops:
            x = calc(eq,op)
            if x == val :
                Nres += 1
                res += val
                break
    return res, Nres

print(prob1())


def calc2(eqs,Ops):
    res = eqs[0]
    for eq,op in zip(eqs[1:],Ops):
        if op == '|':
            res = int(str(res)  + str(eq))
        else:
            res = eval(str(res) + op + str(eq))
    return res


# this works but is very slow, Have some idea of optimising but then the
# operator iteration needs to be rewritten to a kind of graph thing.
def prob2():
    res = 0
    Nres = 0
    cnt = 0
    for val,eq in zip(testvals,eqs):
        cnt += 1
        Nop = len(eq)-1
        Ops = list(itertools.product('+*|',repeat=Nop))
        for op in Ops:
            x = calc2(eq,op)
            if x == val:
                Nres += 1
                res += val
                break
    return res, Nres

# ran in around 5-10 minuets on i7 laptop
print(prob2())
