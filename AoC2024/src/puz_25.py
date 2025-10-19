
with open('data/25.dat') as f:
    a = f.read().strip()
cards = a.split('\n\n')


# Massage the data to the right format 
locks = []
keys = []
for card in cards:
    a = card.split('\n')
    if a[0] == '#####':  # is lock
        lock = [None] * len(a[0])
        for r in range(len(a)):
            for c in range(len(a[0])):
                if a[r][c] == '.' and lock[c] is None :
                    lock[c] = r -1

#        print(lock)
#        print(a)
        locks.append(lock)
    else: #is a key
        key = [None] * len(a[0])
        for r in range(len(a)):
            for c in range(len(a[0])):
                if a[r][c] == '#' and key[c] is None :
                    key[c] = len(a)-(r +1)

#        print(key)
#        print(a)
        keys.append(key)

# Part 1
res = 0
for key in keys:
    for lock in locks:
        if max([a+b for a,b in zip(key,lock)]) <= 5 :
            res +=1
print(res)



