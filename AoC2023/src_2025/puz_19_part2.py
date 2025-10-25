# Detailed comments by Claude.ai

import re
import copy

# Read input: workflows and part ratings separated by blank line
with open('../data/19_data.dat') as f:
#with open('../testdata/19_testdata.dat') as f:
    groups = [group.splitlines() for group in f.read().split('\n\n')]

# For part two we only consider the workflows (not individual ratings)
WFstrings = groups[0]  # Workflow definitions like "px{a<2006:qkd,m>2090:A,rfg}"

WFs = {}  # Dictionary to store parsed workflows
# Map Workflows to a dict
# Result: WFs['px'] = ['a<2006:qkd', 'm>2090:A', 'rfg']
for WF in WFstrings:
    name, roules = WF.split('{')  # Split name from rules
    roules = roules[:-1]           # Remove trailing '}'
    WFs[name] = roules.split(',')  # Split rules into list

# Min Max values for each variable, all inclusive
# Tracks valid ranges: [min, max] for x, m, a, s
bounds = {'x': [1, 4000], 'm': [1, 4000], 'a': [1, 4000], 's': [1, 4000]}

res_bounds = []  # List to accumulate all accepted bound ranges


def evalit(bounds0, WFname, WFIdx):
    """
    Recursively evaluate workflows with range splitting.
    
    Args:
        bounds0: Dict of current valid ranges for x,m,a,s
        WFname: Current workflow name
        WFIdx: Index of rule within workflow to evaluate
    """
    #print(WFname,WFIdx)
    #print(bounds0)
    
    # Base case: reached Accept terminal
    if WFs[WFname][WFIdx] == 'A':
        res_bounds.append(bounds0)
        print(bounds0)
        return
    
    # Base case: reached Reject terminal
    if WFs[WFname][WFIdx] == 'R':
        return
    
    # Default rule (last in workflow) - no condition, just follow target
    if WFIdx == len(WFs[WFname])-1:
        bounds = copy.deepcopy(bounds0)
        evalit(bounds, WFs[WFname][WFIdx], 0)  # Jump to target workflow
        return
    
    # Parse conditional rule: "x<2006:qkd" -> var='x', op='<', num=2006, target='qkd'
    pattern = r'([a-zA-Z]+)([<>])(\d+):([a-zA-Z]+)'
    var, op, num, target = re.match(pattern, WFs[WFname][WFIdx]).groups()
    num = int(num)
    
    # BRANCH 1: Assume we fulfill the rule (condition is TRUE)
    bounds = copy.deepcopy(bounds0)
    if op == '<':
        # If x<2006, constrain upper bound: x must be <= 2005
        if bounds[var][1] >= num:
            bounds[var][1] = num - 1
    else:  # op == '>'
        # If x>2006, constrain lower bound: x must be >= 2007
        if bounds[var][0] <= num:
            bounds[var][0] = num + 1
    
    # Follow the target with constrained bounds
    if target == 'A':
        res_bounds.append(bounds)
        print(bounds)
    elif target == 'R':
        None  # Rejected branch, do nothing
    else:
        evalit(bounds, target, 0)  # Jump to target workflow
    
    # BRANCH 2: Assume we do NOT fulfill the rule (condition is FALSE)
    # Continue to next rule in current workflow with inverted constraint
    bounds = copy.deepcopy(bounds0)
    if op == '<':
        # If NOT x<2006, then x>=2006: constrain lower bound
        if bounds[var][0] < num:
            bounds[var][0] = num 
    else:  # op == '>'
        # If NOT x>2006, then x<=2006: constrain upper bound
        if bounds[var][1] > num:
            bounds[var][1] = num
    
    evalit(bounds, WFname, WFIdx+1)  # Move to next rule in same workflow
    return


# Start evaluation at 'in' workflow with full ranges
evalit(bounds, 'in', 0)

# Calculate total combinations across all accepted ranges
# All solutions should be "orthogonal" (non-overlapping)
res = 0
for bound in res_bounds:
    res0 = 1
    # For each variable, calculate range size and multiply
    for bb in bound.values():
        res0 *= bb[1] - (bb[0] - 1)  # Range size: max - min + 1
    res += res0

print(res)
