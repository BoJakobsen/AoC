import re

# Read input: workflows and part ratings separated by blank line
with open('../data/19_data.dat') as f:
#with open('../testdata/19_testdata.dat') as f:
    groups = [group.splitlines() for group in f.read().split('\n\n')]

WFstrings = groups[0]  # Workflow definitions like "px{a<2006:qkd,m>2090:A,rfg}"
ratings = groups[1]     # Part ratings like "{x=787,m=2655,a=1222,s=2876}"

WFs = {}  # Dictionary to store parsed workflows

# Map Workflows to a dict
# Result: WFs['px'] = ['a<2006:qkd', 'm>2090:A', 'rfg']
for WF in WFstrings:
    name, roules = WF.split('{')  # Split name from rules
    roules = roules[:-1]           # Remove trailing '}'
    WFs[name] = roules.split(',')  # Split rules into list

res = 0  # Accumulator for total rating sum

def evalit(curWF, x, m, a, s):
    """Recursively evaluate workflow rules for a part with ratings x,m,a,s"""
    global res
    
    # Check all conditional rules (all except last which is default)
    for rule in WFs[curWF][:-1]:
        ru, nam = rule.split(':')  # Split condition from target: "a<2006:qkd" -> "a<2006", "qkd"
        
        if eval(ru):  # Evaluate condition like "a<2006" using current x,m,a,s values
            if nam == 'A':  # Accepted
                res += x+m+a+s
                return 
            if nam == 'R':  # Rejected
                return
            evalit(nam, x, m, a, s)  # Follow workflow target
            return
    
    # No conditional matched - use default rule (last item)
    nam = WFs[curWF][-1]
    if nam == 'A':
        res += x+m+a+s
        return 
    if nam == 'R':
        return
    evalit(nam, x, m, a, s)  # Follow default workflow
    return

# due to limitations on the name-space of exec, this cant be encapsulated in a function
# Using exec is not the best solution, but it was fast :-) 
if True:
    for rating in ratings:
        rating = rating[1:-1]  # remove {} from "{x=787,m=2655,a=1222,s=2876}"
        
        for val in rating.split(','):  # Split into ["x=787", "m=2655", "a=1222", "s=2876"]
            exec(val)  # Execute each assignment to create variables x, m, a, s in global scope
        
        evalit('in', x, m, a, s)  # Start evaluation at 'in' workflow
    
    print(res)  # Print total sum of accepted parts
    
