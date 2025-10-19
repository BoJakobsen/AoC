from itertools import product

#with open('../testdata/13_testdata.dat') as f:
with open('../data/13_data.dat') as f:
    a = f.read().strip()
    maps = a.split('\n\n')  # Split on empty line


def findit(mapl):
    for k in range(1, len(mapl)):
        u = k-1
        d = k
        found = True
        while u >= 0 and d < len(mapl):
            # print(u,d,mapl[u],mapl[d])
            if mapl[u] != mapl[d]:
                found = False
                break
            else:
                u -= 1
                d += 1
        if found:
            # print(k, found)
            return k
    return 0

def part1():
    res = 0
    for map0 in maps:

        # convert to list of lists
        mapl = list(map(list, map0.split('\n')))

        # rotated 90 deg
        maplr = list(zip(*mapl))

        res += 100 * findit(mapl)
        res += (findit(maplr))
    print(res)

part1()


# find all possible lines
def findit2(mapl):
    Nreflect = []
    for k in range(1, len(mapl)):
        u = k-1
        d = k
        found = True
        while u >= 0 and d < len(mapl):
            # print(u,d,mapl[u],mapl[d])
            if mapl[u] != mapl[d]:
                found = False
                break
            else:
                u -= 1
                d += 1
        if found:
            # print(k, found)
            Nreflect.append(k)
    return Nreflect


def part2():
    res = 0
    for map0 in maps:

        # convert to list of lists
        mapl = list(map(list, map0.split('\n')))
        maplr = list(zip(*mapl))

        #res0 = set()
        #res0r = set() 

        res0 = 0
        res0r = 0
        a = findit2(mapl)
        if len(a) > 0:
            res0 = (a[0])
        a = findit2(maplr)
        if len(a) > 0:
            res0r = a[0]

        nl = len(mapl)
        nc = len(mapl[0])

        for l, c in product(range(nl), range(nc)):  # for easy break 
            c0 = mapl[l][c]
            if c0 == "#" :
                mapl[l][c] = "."
            else:
                mapl[l][c] = "#"

            # rotated 90 deg
            maplr = list(zip(*mapl))

            res_new = findit2(mapl)
            res_new_r = findit2(maplr)

            mapl[l][c] = c0

            # remove the original solution from set
            if res0 in res_new:
                res_new.remove(res0)
            if res0r in res_new_r:
                res_new_r.remove(res0r)

            if (len(res_new) + len(res_new_r)) == 1:  # check we only have ONE solution
                if len(res_new) == 1:
                    res += 100 * res_new[0]

                if len(res_new_r) == 1:
                    res += res_new_r[0]

                # In hindsight it is clear that each new reflection will show up two times
                # one changing #-> . and one .->#
                # So a break is a solution, or take half (like this better)
                # break

    print(res//2)

part2()
    

# For printing

# print map and rotated map
# for l in mapl:
#     print("".join(l))

# print("")

# for l in maplr:
#     print("".join(l))

