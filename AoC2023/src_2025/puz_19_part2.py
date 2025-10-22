import re
import copy

# Read input: workflows and part ratings separated by blank line
with open('../data/19_data.dat') as f:
#with open('../testdata/19_testdata.dat') as f:
    groups = [group.splitlines() for group in f.read().split('\n\n')]

# for part two we only consider the WF's 
    WFstrings = groups[0]  # Workflow definitions like "px{a<2006:qkd,m>2090:A,rfg}"


WFs = {}  # Dictionary to store parsed workflows

# Map Workflows to a dict
# Result: WFs['px'] = ['a<2006:qkd', 'm>2090:A', 'rfg']
for WF in WFstrings:
    name, roules = WF.split('{')  # Split name from rules
    roules = roules[:-1]           # Remove trailing '}'
    WFs[name] = roules.split(',')  # Split rules into list


# Min Max values, all inclusive
bounds ={'x':[1, 4000], 'm':[1, 4000], 'a':[1, 4000], 's':[1, 4000]}

res_bounds = []

def evalit(bounds0, WFname, WFIdx):
    #print(WFname,WFIdx)
    #print(bounds0)
    if WFs[WFname][WFIdx] == 'A':
        res_bounds.append(bounds0)
        print(bounds0)
        return
    if WFs[WFname][WFIdx] == 'R':
        #print('Reject')
        return
    if WFIdx == len(WFs[WFname])-1:
        bounds = copy.deepcopy(bounds0)
        evalit(bounds,WFs[WFname][WFIdx],0)
        return
    pattern = r'([a-zA-Z]+)([<>])(\d+):([a-zA-Z]+)'
    var, op, num, target = re.match(pattern, WFs[WFname][WFIdx]).groups()
    num = int(num)
    # assume we fulfill the rule
    bounds = copy.deepcopy(bounds0)
    if op == '<':
        if bounds[var][1] >= num:
            bounds[var][1] = num - 1
    else:
        if bounds[var][0] <= num:
            bounds[var][0] = num + 1
    if target == 'A':
        res_bounds.append(bounds)
        print(bounds)
    elif target == 'R':
        None
    else:
        evalit(bounds,target, 0)
    # assume we do not fulfill the criteria
    bounds = copy.deepcopy(bounds0)
    if op == '<':
        if bounds[var][0] < num:
            bounds[var][0] = num 
    else:
        if bounds[var][1] > num:
            bounds[var][1] = num
    evalit(bounds, WFname, WFIdx+1)
    return


evalit(bounds,'in',0)

# Calculate total, all solutions should be "orthogonal"
res = 0
for bound in res_bounds:
    res0 = 1
    for bb in bound.values():
        res0 *= bb[1]-(bb[0]-1)
    res += res0
print(res)


