from collections import defaultdict
import copy

CPU = {}

with open('../data/17.dat') as f:
    lines = [(x.strip()) for x in f]

A = int(lines[0].split(':')[1])
B = int(lines[1].split(':')[1])
C = int(lines[2].split(':')[1])
Prog = list(map(int,lines[4].split(':')[1].split(',')))


def initialize_CPU(A,B,C):
    CPU['A'] = A
    CPU['B'] = B
    CPU['C'] = C
    CPU['PC'] = 0
    CPU['OUT'] = ''

 
def combo(operand):
    if operand <= 3 :
        return operand
    elif operand == 4 :
        return CPU['A']
    elif operand == 5 :
        return CPU['B']
    elif operand == 6 :
        return CPU['C']
    elif operand == 7 :
        print("ERROR: combo 7")


# Define op code to description for easy program printing
ops = {0: 'adv:  A = A >> comb(opr)',  # right bit shift by combo operand
       1: 'blx:  B = B xor opr  ',   # B XOR operand
       2: 'bst:  B = combo(opr) % 8',  # Truncate to 3 bit
       3: 'jnz: jump opr if A =! 0',   # jump if A not 0
       4: 'bxc:  B = B xor C ',   # B Xor C
       5: 'out:  OUT = combo(opr) % 8  ',   # Print
       6: 'bdv:  B = A >> comb(opr) ',   # right bit shift
       7: 'cdv:  C = A >> comb(opr)'   # right bit shift
      }



def RunProg(prog = Prog):
    while CPU['PC'] < len(prog):
        jnz = False
        op = prog[CPU['PC']]
        operand = prog[CPU['PC']+1]

        match op:
            case 0:  # adv
                #  print('adv:', operand)
                CPU['A'] = CPU['A'] // 2**combo(operand)
            case 1:  # blx
                CPU['B'] = CPU['B'] ^ operand
            case 2:  # bst
                CPU['B'] = combo(operand) % 8
            case 3:  # jnz
                if CPU['A'] != 0:
                    jnz = True
                    CPU['PC'] = operand
            case 4:  # bxc
                CPU['B'] = CPU['B'] ^ CPU['C']
            case 5:  # out
                if CPU['OUT'] == '':
                    CPU['OUT'] += str(combo(operand) % 8)
                else:
                    CPU['OUT'] = CPU['OUT'] + ',' + str(combo(operand) % 8)
            case 6:  # bdv
                CPU['B'] = CPU['A'] // 2**combo(operand)
            case 7:  # cdv
                CPU['C'] = CPU['A'] // 2**combo(operand)
#        print(op, operand)
        if not jnz:
            CPU['PC'] += 2  # Advance PC if not jnz command


# Test Part A still works
initialize_CPU(A, B, C)
RunProg()
print(CPU['OUT'])  # Output is now a string 
# order of output is left to right


# Part B, test data, should output itself
ProgB_test = [0,3,5,4,3,0] 

A_test = 117440
B_test = 0
C_test = 0
initialize_CPU(A_test, B_test, C_test)
RunProg(ProgB_test)
print(CPU['OUT']) # 0,3,5,4,3,0
# works and is in right order

# Print program, for inspection
for kk in list(range(0,len(Prog),2)):
    print(ops[Prog[kk]], end='' )
    print(' : ', Prog[kk+1])


# Program, with combo operands converted to registers manually
# [2, 4, 1, 3, 7, 5, 4, 1, 1, 3, 0, 3, 5, 5, 3, 0]
#
# bst:  B = combo(opr) % 8 :  A   : 3 last bits of A -> B
# blx:  B = B xor opr      :  3   : B xor 3 (0b011) -> B 
# cdv:  C = A >> comb(opr) :  B   : A right shift by B -> C (B can be 0 to 7)
# bxc:  B = B xor C  :            : B xor C -> B
# blx:  B = B xor opr   :     3   : B xor 3 (0b011) -> B
# adv:  A = A >> comb(opr) :  3   : Right shift A (next 3 bit word)
# out:  OUT = combo(opr) % 8  B   : Print result B (3bit)
# jnz: jump opr if A =! 0 :  0    : Repeat if A is not 0

# Observations which might be general:
#    Only one jump at the end, goes to start if A is not 0
#    Only one out
#    A is "used" 3 bits per cycle

# Furthermore one can based in the concrete program, or on the existing op codes
# conclude that if the above 3 statements are true, any output will only
# depend on current last three bits of A and higher order bits


# Returns binary representation of a as a 3 bit string, padded by 0's
# (there possible is a better way to work with binary numbers, that using strings)
def tobin(a):
    ab = bin(a)[2:]
    if len(ab) == 1 : ab = '00' + ab
    if len(ab) == 2 : ab = '0' + ab
    return(ab)


# If we know "higher order" bits (A_bef), we can try to find all 3 bit number
# (0-7) which results in the wished output (num)
# There might be multiple one or 0 possible such numbers
def findmatch(A_bef,num):
    Matchs = []
    A0 = ''
    for AA in A_bef:
        A0 = A0 + tobin(AA)
    for aa in range(8):
        # In this version my program is hard coded in
        A = int(A0 + tobin(aa),2)
        B = A % 8
        B = aa  ^ 3
        C = A // 2**B
        B = B ^C
        B = B ^3
        B = B % 8
#        print(B)
        if B == num:
            Matchs.append(aa)
    return Matchs

# We can now try to work from highest bits in A, corresponding to last number in Prog
# for the first 3bits we know that any higher bits are 0 (otherwise this wouldn't be
# the highest bits)

# Prog for inspection [2, 4, 1, 3, 7, 5, 4, 1, 1, 3, 0, 3, 5, 5, 3, 0]

findmatch([],0)  # [0, 3]  0 doesn't work as the program would then have terminated

findmatch([3],3)  # [0]

As = [3, 0]
findmatch(As, 5) [4]

As = [3, 0, 4]
findmatch(As,5) # [5,7] 5 works in next point

As = [3, 0, 4, 5]
findmatch(As,3) # [1]

As = [3, 0, 4, 5, 1]
findmatch(As,0) # [3,5] # Choose 3 "randommly"

As = [3, 0, 4, 5, 1, 3]
findmatch(As,3) # [0]

As = [3, 0, 4, 5, 1, 3, 0]
findmatch(As,1) # [1, 4] # Choose 4 "randommly"

As = [3, 0, 4, 5, 1, 3, 0, 4]
findmatch(As,1) # [1]

As = [3, 0, 4, 5, 1, 3, 0, 4, 1]
findmatch(As,4) # []

# So we need to backtrack, lets try recursion

# We work with the program in revers (just to make indexing more easy )
Prog_Rev = Prog[::-1]

# Same as findmatch, just using a "n" which indexes into Prog_rev
def findmatch2(A_bef,n):
    num = Prog_Rev[n]
    Matchs = []
    A0 = ''
    for AA in A_bef:
        A0 = A0 + tobin(AA)
    for aa in range(8):
        A = int(A0 + tobin(aa),2)
        B = A % 8
        B = aa  ^ 3
        C = A // 2**B
        B = B ^C
        B = B ^3
        B = B % 8
        if B == num:
            Matchs.append(aa)
    return Matchs

res = []
def calcit(A_bef,n):
    print(n, ':', A_bef)
    if n == len(Prog_rev):  # We reached the end of Prog
        res.append(A_bef)   # Append resulting number to res
        return
    As = findmatch2(A_bef, n)
    for A in As:
        if n == 0 and A ==0: continue # for n = 0 we need to skip this
        A_new = copy.copy(A_bef)
        A_new.append(A)
        calcit(A_new, n+1)
    return

calcit([],0)
len(res)
# I found a unique solution, so this must be the lowest number

# unpack the 3bit parts and combin to one binery number
A = ''
for AA in res[0]:
    A = A + tobin(AA)

initialize_CPU(int(A,2), B, C)
RunProg(Prog)
print(CPU['OUT']) #  2,4,1,3,7,5,4,1,1,3,0,3,5,5,3,0

print(int(A,2)) # 

