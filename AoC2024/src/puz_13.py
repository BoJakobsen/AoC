# Run Snippets.py before to load stuff

lines = baseloader('../data/13.dat')
# 3 lines one blank


## Problem 1
res = 0
st = list(range(0,len(lines),4))
for kk in st:#   
    tmp=lines[kk].split(':')[1].split(',')
    M11 = int(tmp[0][3:])
    M21 = int(tmp[1][3:])
    tmp=lines[kk+1].split(':')[1].split(',')
    M12 = int(tmp[0][3:])
    M22 = int(tmp[1][3:])
    tmp=lines[kk+2].split(':')[1].split(',')
    Y1 = int(tmp[0][3:])
    Y2 = int(tmp[1][3:])


    M= np.array([[M11, M12],[M21, M22]])
    Y = np.array([Y1, Y2])
    X = np.linalg.solve(M,Y)    
    if (np.abs(np.round(X[0]) - X[0]))<1e-9 and (np.abs(np.round(X[1]) - X[1]))<1e-9  and X[0]<=100 and X[1] <=100:
#        print(X)
        res += X[0]*3 + X[1]
#        print(kk)
print(res)
 
##
## Problem 2
res = 0
st = list(range(0,len(lines),4))
for kk in st:#   
    tmp=lines[kk].split(':')[1].split(',')
    M11 = int(tmp[0][3:])
    M21 = int(tmp[1][3:])
    tmp=lines[kk+1].split(':')[1].split(',')
    M12 = int(tmp[0][3:])
    M22 = int(tmp[1][3:])
    tmp=lines[kk+2].split(':')[1].split(',')
    Y1 = int(tmp[0][3:]) + 1e13
    Y2 = int(tmp[1][3:]) + 1e13


    M= np.array([[M11, M12],[M21, M22]])
    Y = np.array([Y1, Y2])
    X = np.linalg.solve(M,Y)
#    print(X)
#    print(np.abs(np.round(X[0]) - X[0]))
    if (np.abs(np.round(X[0]) - X[0]))<1e-3 and (np.abs(np.round(X[1]) - X[1]))<1e-1 :
        res += X[0]*3 + X[1]
print(res)
 
