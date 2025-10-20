import re

# Multiple groups
with open('../data/19_data.dat') as f:
#with open('../testdata/19_testdata.dat') as f:
    groups = [group.splitlines() for group in f.read().split('\n\n')]

WFstrings = groups[0]
ratings = groups[1]

WFs = {}
# Map Workflows to a dict
for WF in WFstrings:
    name, roules = WF.split('{')
    roules = roules[:-1]
    WFs[name] = roules.split(',')

res = 0


def evalit(curWF, x, m, a, s):
    global res
    for rule in WFs[curWF][:-1]:
        ru, nam = rule.split(':')
        if eval(ru):
            if nam == 'A':
                res += x+m+a+s
                return 
            if nam == 'R':
                return
            evalit(nam, x, m, a, s)
            return
    nam = WFs[curWF][-1]
    if nam == 'A':
        res += x+m+a+s
        return 
    if nam == 'R':
        return
    evalit(nam, x, m, a, s)
    return

# due to limitations on the name-space of exec, this cant be encapsulated in a function
# Using exec is not the best solution, but it was fast :-) 
if True:
    for rating in ratings:
        rating = rating[1:-1] # remove {}
        for val in rating.split(','):
            exec(val)  # assign values
        evalit('in', x, m, a, s)
    print(res)     
