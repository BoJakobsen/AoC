#with open('../data/03_testdata.dat') as f:
with open('../data/03_data.dat') as f:
    banks = [x.strip() for x in f]


def prob1Only():
    res = 0
    for bank in banks:
        nums = list(map(int, bank))
        maxfirst = max(nums[:-1])  # max first digit (has to have at least one left)
        maxsecond = max(nums[nums.index(maxfirst)+1:])  # Max second digit (after the first)
        maxnum = str(maxfirst) + str(maxsecond)
        res += int(maxnum)
    print('Problem 1: ', res)


prob1Only()


def prob(N):
    """Find largest N-digit number preserving order from each bank."""
    res = 0
    for bank in banks:
        nums = list(map(int, bank))
        maxjol = []
        start_idx = 0

        for k in range(N):
            # We need N-k more digits, so can only look at positions
            # that leave enough remaining digits
            end_idx = len(nums) - (N - k) + 1
            chunk = nums[start_idx:end_idx]

            # Greedily pick the largest digit in valid range
            max_digit = max(chunk)
            maxjol.append(max_digit)

            # Next search starts after the chosen digit
            start_idx = start_idx + chunk.index(max_digit) + 1

        res += int(''.join(map(str, maxjol)))

    print(f'Max joltages for {N} batteries: {res}')


# Solve both parts
prob(2)
prob(12)
