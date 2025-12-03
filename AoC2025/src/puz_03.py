#with open('../data/03_testdata.dat') as f:
with open('../data/03_data.dat') as f:
    banks = [x.strip() for x in f]

def prob1Only():
    res = 0
    for bank in banks:
        nums = list(map(int,bank))
        maxfirst = max(nums[:-1])  # max first digit (has to have at least one left)
        maxsecond = max(nums[nums.index(maxfirst)+1:])  # Max second digit (after the first)
        maxnum = str(maxfirst) + str(maxsecond)
        res += int(maxnum)
    print('Problem 1: ', res)

#prob(1)


def prob(N):
    res = 0
    for bank in banks:  # Loop over the battery banks
        nums = list(map(int, bank))  # Convert bank info to integers 
        maxjol = [None] * N  # array for constructing largest possible joltage
        lastidx = 0  # Index for last used digit
        for k in range(N):  # loop over requested number of digits
            nums_part = nums[lastidx:len(nums)-(N-k)+1]  # extract usable part
            maxjol[k] = max(nums_part)  # Find max number in usable part
            lastidx = nums_part.index(maxjol[k])+1+lastidx  # Update index
        res += int(''.join(map(str, maxjol)))  # convert back to number and add up
    print('Max joltages for ', N, ' bateries: ', res)


# Both parts can now be solved
prob(2)
prob(12)
