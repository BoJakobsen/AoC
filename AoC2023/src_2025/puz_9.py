#with open('../testdata/9_testdata.dat') as f:
with open('../data/9_data.dat') as f:
    report = [list(map(int,list(x.split()))) for x in f]
# load as list of lists


# Efficient diff of a list using zip operator
def diff(dat):
    res =  [y - x for x, y in zip(dat,dat[1:])]
    return res


def part1():
    res = 0
    for hist in report:
        # Diff until all differences are 0
        all_zero = False
        end_val = [hist[-1]]  # store the last value of each step
        while not all_zero:
            hist = diff(hist)
            end_val.append(hist[-1])
            if set(hist) == set([0]):  # test if hist is all 0
                all_zero = True
        # do the extrapolation
        next_val = 0
        for val in end_val[::-1]:
            next_val += val
        res += next_val  # sum up result
    print(res)


part1()
