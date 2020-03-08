import time 
import sys
import numpy as np
import matplotlib.pyplot as plt

# Plotting functions

def Plotvec1(u, z, v):
    
    ax = plt.axes()
    ax.arrow(0, 0, *u, head_width=0.05, color='r', head_length=0.1)
    plt.text(*(u + 0.1), 'u')
    
    ax.arrow(0, 0, *v, head_width=0.05, color='b', head_length=0.1)
    plt.text(*(v + 0.1), 'v')
    ax.arrow(0, 0, *z, head_width=0.05, head_length=0.1)
    plt.text(*(z + 0.1), 'z')
    plt.ylim(-2, 2)
    plt.xlim(-2, 2)

def Plotvec2(a,b):
    ax = plt.axes()
    ax.arrow(0, 0, *a, head_width=0.05, color ='r', head_length=0.1)
    plt.text(*(a + 0.1), 'a')
    ax.arrow(0, 0, *b, head_width=0.05, color ='b', head_length=0.1)
    plt.text(*(b + 0.1), 'b')
    plt.ylim(-2, 2)
    plt.xlim(-2, 2)

    
a = ["0", 1, "two", "3", 4]
print("a[0]:", a[0])
print("a[1]:", a[1])


print("=================")

b =np.array([1,2,3,4,5,6,7,8])
print(b[3])

print("=================")

select = [1,4,6]
c = b[3:7]
print(select,c)

d = b[select]
print(d)

b[select]=1000
e=b[select]
print(e,b)

sd = b.std()
mn = b.mean()
print(sd,mn)

u = np.array([1, 0])
v = np.array([0,1])
z = u + v
w = u*v
x = np.dot(u,v)
y = 2*v
print(u,v,z,w,x,y)

aa = np.array([np.pi, np.pi/2,np.pi])
bb = np.sin(aa)
print(bb)

cc = np.linspace(-5,5,num=5)
print(cc)

a = np.array([1, 1])
b = np.array([0, 1])
Plotvec2(a, b)
print("The dot product is", np.dot(a, b))
print("The dot product is", np.dot(a, b))
u

