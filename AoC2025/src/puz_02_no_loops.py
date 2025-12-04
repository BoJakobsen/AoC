import math
#with open('../data/02_testdata.dat') as f:
with open('../data/02_data.dat') as f:
    rangestxt = [x.strip().split(',') for x in f]

# Code commented by Claude.ai
    
# Convert data to list of [start, end] pairs (as strings)
ranges = []
for r in rangestxt[0]:
    ranges.append(list((r.split('-'))))

# Assumption: start and end differ by at most 1 digit length
# (e.g., 9999 to 10001, not 99 to 100000)


def find_repeat(r):
    """Find sum of all numbers with exact 2-fold repetition in range [r[0], r[1]].

    Uses arithmetic series formula instead of looping through all numbers.
    Assumes start and end have same number of digits.
    """
    # Both must have same length
    if len(r[0]) != len(r[1]):
        return 0

    # Total length must be even (for 2-fold repetition)
    if len(r[0]) % 2 != 0:
        return 0

    rep_len = int(len(r[0])/2)  # Length of the repeating pattern

    # Find first valid pattern by comparing halves of range start
    # If first_half >= second_half, then pattern*mask >= range_start (e.g., 123123 >= 123120)
    # If first_half < second_half, then pattern*mask < range_start (e.g., 123123 < 123456)
    # so we need the next pattern
    if int(r[0][0:rep_len]) >= int(r[0][rep_len:]):
        start = int(r[0][0:rep_len])  # This pattern is >= range start
    else:
        start = int(r[0][0:rep_len]) + 1  # Need next pattern

    # Find last valid pattern by comparing halves of range end
    # If first_half <= second_half, then pattern*mask <= range_end (e.g., 125125 <= 125130)
    # If first_half > second_half, then pattern*mask > range_end (e.g., 125125 > 125120)
    # so we need the previous pattern
    if int(r[1][0:rep_len]) <= int(r[1][rep_len:]):
        end = int(r[1][0:rep_len])  # This pattern is <= range end
    else:
        end = int(r[1][0:rep_len]) - 1  # Need previous pattern

    # Create multiplier: pattern 'abc' becomes 'abcabc' via pattern * 1001
    # For rep_len=3: '1001', rep_len=2: '101', etc.
    mask = '1' + '0' * (rep_len-1) + '1'

    # Sum of arithmetic sequence: sum(start to end) * mask
    # Sum of patterns = (first + last) * count / 2, where count = (end - start + 1)
    # Then multiply by mask to get sum of actual repeated numbers
    res = int(((int(start) + int(end))*(int(end)-int(start)+1)/2)*int(mask))
    return res


res = 0
for r in ranges:
    # If start and end have different digit counts, split at boundary
    # (e.g., 9999 and 10001 split into [9999,9999] and [10000,10001])
    if len(r[0]) != len(r[1]):
        midtpoint = int('9' * len(r[0]))  # Largest number with start's digit count
        res += find_repeat([r[0], str(midtpoint)])
        res += find_repeat([str(midtpoint+1), r[1]])
    else:
        res += find_repeat(r)

print(res)
