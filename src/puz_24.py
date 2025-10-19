from collections import defaultdict

with open('../data/24.dat') as f:
    lines = [(x.strip()) for x in f]

defwires = defaultdict(int)
gates = defaultdict(int)
undefwires = set()

kk =0
for line in lines:
    if line == '': break
    a,b = line.split(': ')
    defwires[a] = int(b)
    kk += 1

for line in lines[kk+1:]:
    a,b = line.split(' -> ')
    gates[b] = a.split(' ')
    undefwires.add(b)


# Part 1

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


# calc decimal number from "z" wires
kk = 0
res = 0
for _, b in sorted(output):
    res += b*2**kk
    kk += 1
print(res)


