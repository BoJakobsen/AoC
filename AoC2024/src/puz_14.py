import numpy as np
import matplotlib.pyplot as plt
import copy 
import time

with open('../data/14.dat') as f:
    lines = [(x.strip()) for x in f]

pos0 = []
vel = []
for line in lines:
    p,v = line.split()
    p = tuple(map(int,p[2:].split(',')))
    v = tuple(map(int,v[2:].split(',')))
    pos0.append(p)
    vel.append(v)
 
# for demo set.
# width = 11
# height = 7

# For dataset.
width = 101
height = 103


# Advance N*V and handle periodic boundary conditions
def advance(pos0, vel, N):
    pos = [((p[0] + v[0]*N) % width, (p[1] + v[1]*N) % height ) for p,v in zip(pos0,vel) ]
    return pos


# Index the the quadrants (not standard numbering)
def quadrant(p):
    if p[0] <= np.floor(width/2)-1 and  p[1] <= np.floor(height/2)-1:
        return 1
    if p[0] >= np.ceil(width/2) and  p[1] <= np.floor(height/2)-1:
        return 2
    if p[0] <= np.floor(width/2)-1 and  p[1] >= np.ceil(height/2):
        return 3
    if p[0] >= np.ceil(width/2) and  p[1] >= np.ceil(height/2):
        return 4
    return 0

# Problem  1 
N = 100  # Advance 100 steps
pos = advance(pos0,vel,N)

# calculate  result
q = list(map(quadrant, pos))
res = 1
for k in [1, 2, 3, 4]:
    res *= q.count(k)
print(res)

# Problem 2, try to plot each step

f = plt.figure()
ax = f.subplots()
pos = copy.copy(pos0)

for N in range(1,400):
    pos = advance(pos,vel,1)
    ax.clear()
    ax.scatter(*zip(*pos))
    f.show()
    print(N)
    input("key")
    #plt.pause(0.2)

# hint from wrong guess: is that it is more than 399, so...

# Try to look at data other way
# record number of points in  each quadrant,
# assuming we see something at the "Christmas three"
pos = copy.copy(pos0)
qdat = [[],[],[],[],[]]
for N in range(1,10000):
    pos = advance(pos,vel,1)
    q = list(map(quadrant, pos))
    for k in [0, 1, 2, 3, 4]:
        qs = q.count(k)
        qdat[k].append(qs)

f = plt.figure()
ax = f.subplots()
for kk in range(0,5):
    ax.plot(qdat[kk], label=str(kk))
ax.legend()
plt.show()

# 6888 (remember the axis starts at 0)
# sticks somewhat out (not very clear, but got a bit lucky and looked at it)

N=6888
f = plt.figure()
ax = f.subplots()
pos = copy.copy(pos0)
pos = advance(pos,vel,N)
ax.scatter(*zip(*pos))
f.show()

# No automated solution for general inputs, maybe one can search for the peak
# but that will require that we look at other inputs to understand this.


