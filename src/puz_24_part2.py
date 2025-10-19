from collections import defaultdict

with open('../data/24.dat') as f:
    lines = [(x.strip()) for x in f]

defwires = defaultdict(int)
gates = defaultdict(int)
undefwires = set()

inpX = set()
inpY = set() 
output = set()

kk =0
for line in lines:
    if line == '': break
    a,b = line.split(': ')
    defwires[a] = int(b)
    kk += 1
    if a[0] == 'x':
        inpX.add((a,b))
    if a[0] == 'y':
        inpY.add((a,b))

for line in lines[kk+1:]:
    a,b = line.split(' -> ')
    gates[b] = a.split(' ')
    undefwires.add(b)


# Part 2
def calcit(defwires, gates, undefwires):
    output = set()
    while len(undefwires) > 0:
        for wir, calc in gates.items():
            if wir not in undefwires: continue  # Already defined
            if calc[0] in defwires and calc[2] in defwires:
                match calc[1]:
                    case 'AND':
                        res = defwires[calc[0]] & defwires[calc[2]] 
                    case 'OR':
                        res = defwires[calc[0]] | defwires[calc[2]] 
                    case 'XOR':
                        res = defwires[calc[0]] ^ defwires[calc[2]]
                defwires[wir] = res
                undefwires.remove(wir)
                if wir[0] == 'z':
                    output.add((wir,res))
    return output


# Helperfunction 
def binnum(X):
    out = ''
    for _, a in sorted(X,reverse = True):
        out += str(a)
#        print(a,end = '' )
#    print('')
    outint = int(out,2)
    return out , outint


output = calcit(defwires, gates, undefwires)


# this is properly a standard full adder
# So in general
# sum = (X ^ B) ^Cin
# Cout = (X & B) or (Cin & (X ^B))


outs=set()
couts=[''] * 45
couts[0] = 'pjf' # Manually checked bit 0
tmp1 = 0
tmp2 = 0
#for num in [1]:#range(1,45):
for num in range(1,45):
    err = False
    #num = 1
    inpX = f"x{num:02d}"
    inpY = f"y{num:02d}"
    outZ = f"z{num:02d}"

    print(num)
    print('cin:', couts[num-1])
    for out, logic in gates.items():
        x, gate , y = logic
        if inpX in {x, y} and inpY in {x,y}: # x,y input to full adder
            if gate == 'XOR':
                XxorY = out
                print('xor: ', out, x, gate, y)
            elif gate == 'AND':
                XandY = out
                print('and: ' , out, x, gate, y)
            else:
                print('ERROR')
    # check expression for outZ
    a, gate, b = gates[outZ]
    print('out: ', outZ, a, gate, b )
    if not (a in {XxorY, couts[num-1]}) and (b in {XxorY, couts[num-1]}):
        err = True
    # Check out calc 
    for out, logic in gates.items():
        x, gate , y = logic
        if XxorY in {x, y} and gate == 'XOR': # this should now be output    #        
            print('out: ', out, x, gate, y )
            if not couts[num-1] in {x, y}:
                print(out, " wrong Cari")
                outs.add(couts[num-1])
                err = True
            if  out != outZ :
                print(out, "wrong out")
                outs.add(out)
                err = True
            break

    # second part of Cout
    for out, logic in gates.items():
        x, gate , y = logic
        if XxorY in {x ,y}  and gate == 'AND':
            print('co2: ', out, x, gate, y )
            cout2 = out
            if not couts[num-1] in {x, y}:
                err = True
            break
    for out, logic in gates.items():
        x, gate , y = logic
        if cout2 in {x ,y}  :
            print('cou: ' , out, x, gate, y   )
            if XandY not in {x ,y}:
                err = True
                print(out)
                outs.add(XandY)
            couts[num] = out
            break

    if err: input('key')

# z45 is just cout from last calculation, seems good.

    
# The loop will find error, but also false errors (typical in the "next" block)
# Manually inspection is needed to figure out the details.


# manually fixing it, a bit by bit looking at debug output
#
# 5
# z05 y05 AND x05   # this is the AND line
# gdd knc XOR wcq   # this is the out line

# 9
#  z09 kvg OR sgj # this is the cout line
#  cwt jnf XOR wgh # this the the out line

# 20 
# These two seems swaped: 
# css y20 AND x20
# jmv y20 XOR x20
#

# 37
# z37 vcr AND nwb   # this is co2 not out
# pqt vcr XOR nwb   # this must be out 


','.join(sorted(['z05', 'gdd', 'z09', 'cwt' , 'css' , 'jmv', 'z37' , 'pqt']))
