import sympy as sp
import numpy 

# setup algebraic solution for part 2
x1,t1,v1 = sp.symbols('x1 t1 v1')
x2,t2,v2 = sp.symbols('x2 t2 v2')
y1,w1 = sp.symbols('y1 w1')
y2,w2 = sp.symbols('y2 w2')

# x part
eq1_1 = sp.sympify(x1+t1*v1)
eq1_2 = sp.sympify(x2+t2*v2)
# ypart
eq2_1 = sp.sympify(y1+t1*w1)
eq2_2 = sp.sympify(y2+t2*w2)

# equations for findint t1,t2 for intersect
eq1=sp.Eq(eq1_1,eq1_2)
eq2=sp.Eq(eq2_1,eq2_2)
res=sp.solve([eq1,eq2],(t1,t2),dict=True)

#equation for intersect
xeq=eq1_1.subs(t1,res[0][t1])
yeq=eq2_1.subs(t1,res[0][t1])


#Make Python / numpy function for evaluatin all the data
xeqf=sp.lambdify([x1,y1,v1,w1,x2,y2,v2,w2],xeq, "numpy")
yeqf=sp.lambdify([x1,y1,v1,w1,x2,y2,v2,w2],yeq, "numpy")
t1eqf=sp.lambdify([x1,y1,v1,w1,x2,y2,v2,w2],res[0][t1], "numpy")
t2eqf=sp.lambdify([x1,y1,v1,w1,x2,y2,v2,w2],res[0][t2], "numpy")


# load dataset
#with open('testdata/24_testdata.dat') as f:
with open('data/24_data.dat') as f:
    lines=[x.strip() for x in f]

coords=[]
vels=[]
for line in lines: 
    coordstr, velstr = line.split('@')
    coord=list(map(int,coordstr.split(',')))
    vel=list(map(int,velstr.split(',')))
    coords.append(coord)
    vels.append(vel)

MIN=200000000000000
MAX=400000000000000
cnt=0
#loop over all pairs
for k in range(len(coords)):
    for kk in range(k+1,len(coords)):
        coord1=coords[k]
        vel1=vels[k]
        coord2=coords[kk]
        vel2=vels[kk]               
        if vel1[0]/vel1[1]==vel2[0]/vel2[1]: #Check for paralel
            print(k,kk,'Paralel')            
        else: #Calculate intersection
            t1=t1eqf(coord1[0],coord1[1],vel1[0],vel1[1],coord2[0],coord2[1],vel2[0],vel2[1])
            t2=t2eqf(coord1[0],coord1[1],vel1[0],vel1[1],coord2[0],coord2[1],vel2[0],vel2[1])     
            x=xeqf(coord1[0],coord1[1],vel1[0],vel1[1],coord2[0],coord2[1],vel2[0],vel2[1])
            y=yeqf(coord1[0],coord1[1],vel1[0],vel1[1],coord2[0],coord2[1],vel2[0],vel2[1])
            if t1<0 or t2<0:
                print(k,kk,'in Past')                    
            elif x<MIN or x>MAX or y<MIN or y>MAX:                        
                print(k,kk,x,y,'OUTSIDE')
            else: 
                print(k,kk,x,y,'OK')
                cnt+=1
print('Fine: ', cnt)