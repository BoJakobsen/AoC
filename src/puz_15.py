

def HASH(string):
    val=0
    for ch in string:
        val += ord(ch)
        val *=17
        val = val % 256
    return val

def part1():
    # as input is one long line, read one char at the time
    #with open('testdata/15_testdata.dat') as f:
    with open('data/15_data.dat') as f:
        sumit=0    
        while True:
            string=''
            ch=f.read(1)        
            if not ch:
                break
            while (ch !=',')  and (ch !='\n'):
                string+= ch
                ch=f.read(1)
                if not ch:
                    break
            HASHVal= HASH(string)
            sumit+=HASHVal
            #print(string,HASHVal)
    print(sumit)

part1()

def part2():
    #dict the boxs 
    boxs={x:[] for x in range(256) }
    # as input is one long line, read one char at the time
    #with open('../testdata/15_testdata.dat') as f:
    with open('../data/15_data.dat') as f:
    #    sumit=0    
        while True:
            string=''
            ch=f.read(1)        
            if not ch:
                break
            while (ch !=',')  and (ch !='\n'):
                string+= ch
                ch=f.read(1)
                if not ch:
                    break
            if string.find('=')>=0 : # case of assigning
                N=string.find('=')
                lab=string[0:N]
                box=boxs[HASH(lab)]
                fl=string[N+1:]
                found=False
                for Nlens in range(len(box)):
                    if box[Nlens][0] == lab:
                        box[Nlens]=[lab, fl]
                        found=True
                if not found:
                    box.append([lab, fl])            
            elif string.find('-')>=0 : # case of removing
                N=string.find('-')
                lab=string[0:N]
                box=boxs[HASH(lab)]
                for Nlens in range(len(box)):
                    if box[Nlens][0] == lab:
                        box.pop(Nlens)
                        break
            else :
                print('ERROR') 
   
    sumit=0
    for key,box in boxs.items():
        for Nlens,lens in enumerate(box) :
            power = (int(key)+1)*(Nlens+1)*int(lens[1]) 
            sumit+= power
    print(sumit)

part2()
