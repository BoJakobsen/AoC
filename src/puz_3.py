import re

# Just demo lines for prob1 and 2
#lines =[ "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"]
#lines = ["xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"]

with open('../data/3.dat') as f:
    lines=[x.strip() for x in f]


def prob1():
    result = 0
    for line in lines:
         cmds = re.findall("mul\([0-9]{1,3},[0-9]{1,3}\)",line)
         for cm in cmds:
              nums = list(map(int,(cm[4:-1]).split(',')))
              result += nums[0]*nums[1]
    return result


print(prob1())

def prob2(): 
    result = 0
    enab = True # enable state, start with True
    for line in lines:
         cmds = re.findall("(mul\([0-9]{1,3},[0-9]{1,3}\))|(do\(\))|(don't\(\))",line)
         for cm in cmds:
             if cm[1] : # do() cmd
                 enab = True
             if cm[2] : # don't() cmd
                 enab = False
             if enab and cm[0] : #mul(x,y) cmd, only if in enable state
                 nums = list(map(int,(cm[0][4:-1]).split(',')))
                 result += nums[0]*nums[1]

    return result

print(prob2())
