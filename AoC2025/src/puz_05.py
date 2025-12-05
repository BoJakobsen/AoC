# Comments mainly by Claude.ai

# Multiple groups, returned as a list of lists of strings
#with open('../data/05_testdata.dat') as f:
with open('../data/05_data.dat') as f:
    groups = [group.splitlines() for group in f.read().split('\n\n')]

ingredientIDs = list(map(int,groups[1]))  # List of individual IDs to check
fressIDranges = [list(map(int, gr.split('-'))) for gr in  groups[0] ]  # List of [start, end] ranges


# Part 1: Count how many ingredient IDs fall within any freshness range
def part1():
    res = 0
    for ID in ingredientIDs:
        for r in fressIDranges:
            if ID in range(r[0], r[1]+1):
                res += 1
                break  # Each ID only counts once, even if in multiple ranges
    print("Prob 1: ", res)

    
part1()


#  Part 2: Merge overlapping ranges, then count total coverage
def meargeRanges(fressIDranges):
    """Merge overlapping or touching ranges.
 
    Checks if either endpoint of new range falls within existing merged range.
    """
    meargedRanges = []
    for r in fressIDranges:
        mearged = False
        for mr in meargedRanges:
            # Check if r overlaps with mr (either start or end of r is within mr)
            if (r[0] in range(mr[0], mr[1]+1)) or (r[1] in range(mr[0], mr[1]+1)):
                # Extend mr to cover both ranges
                mr[1] = max([mr[1], r[1]])
                mr[0] = min([mr[0], r[0]])
                mearged = True
                break
        if not mearged:
            meargedRanges.append(r.copy())  # Add as new separate range
    return meargedRanges


def part2(fressIDranges):
    """Merge all overlapping ranges until no more merges possible.

    Key insight: iterate both forward and backward to catch fully overlapping ranges
    where one range is completely inside another. (help from a colleague)
    """
    newIDranges = meargeRanges(fressIDranges)

    # Keep merging until convergence (no changes between iterations)
    while newIDranges != fressIDranges:
        fressIDranges = newIDranges
        newIDranges = meargeRanges(fressIDranges)
        newIDranges = meargeRanges(newIDranges[::-1])  # Backward pass for fully overlapping ranges
        newIDranges = newIDranges[::-1]  # Restore original order

    # Sum up the total coverage of all merged ranges
    res = 0
    for r in newIDranges:
        res += r[1]-r[0]+1  # Count of IDs in this range (inclusive)
    print('Part 2: ', res)


part2(fressIDranges)



def part2_sort(fressIDranges):
    """Merge all overlapping ranges until no more merges possible.

       Much easier, sort the list of ranges first. (Hint from Hyperneutrino)
    """
    
    # Sorting ensures handeling of fully overlapping regions 
    fressIDranges = sorted(fressIDranges)

    # Initial merge
    newIDranges = meargeRanges(fressIDranges)
    # Keep merging until convergence (no changes between iterations)
    while newIDranges != fressIDranges:
        fressIDranges = newIDranges
        newIDranges = meargeRanges(fressIDranges)

    # Sum up the total coverage of all merged ranges
    res = 0
    for r in newIDranges:
        res += r[1]-r[0]+1  # Count of IDs in this range (inclusive)
    print('Part 2: ', res)


part2_sort(fressIDranges)

