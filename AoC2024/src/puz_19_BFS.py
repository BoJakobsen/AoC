# this is way to slow, works in principle.
# I did a recursive implementation which by use of cache is much faster
# Maybe this can also be improved similarly


from collections import deque

with open("../data/19.dat") as f:
    for line in f:
        if line.isspace(): break
        towels = line.strip().split(",")

    designs = [line.strip() for line in f]


for kk in range(len(towels)):
    towels[kk] = towels[kk].strip() 

# do a simple BFS on the designs     
res = 0
for design in designs: 
    useabeltow = []
    for towel in towels:
        if towel in design:
            useabeltow.append(towel)

    q = deque([('', -1)])
    seen = {(('', -1))}

    solved = False
    while q and not solved:
        two, last = q.popleft() 
        for ntow in useabeltow:
            nlast = last + len(ntow)        
            if ntow == design[last+1:nlast+1]:
    #        if (ntow, nlast) in seen: continue
                if nlast == len(design)-1:
                    solved = True
    #                print("done")
    #            seen.add((ntwo, nlast))
                q.append((ntow, nlast))

    print(design,solved)
    if solved:
        res += 1
print(res)
