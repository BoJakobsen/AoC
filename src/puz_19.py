#from functools import cache 
# alternative 
with open("../data/19.dat") as f:
    for line in f:
        if line.isspace(): break
        towels = line.strip().split(",")

    designs = [line.strip() for line in f]


for kk in range(len(towels)):
    towels[kk] = towels[kk].strip() 

#@cache
cache = {} # This is needed, work very well, got it from Neil Thistlethwaite 
# do a recursive solution
def testit(design):
    if len(design) == 0:
        return 1
    if design in cache:
        return cache[design]
    res = 0
    for tow in towels:
        if design.startswith(tow):
            tmp = testit(design[len(tow):])
            cache[design[len(tow):]] = tmp
            res += tmp
    return res

res_1 = 0
res_2 = 0
for design in designs:
    tmp = testit(design)
    res_1 += 1
    res_2 += tmp

print(res_1)
print(res_2)
        
