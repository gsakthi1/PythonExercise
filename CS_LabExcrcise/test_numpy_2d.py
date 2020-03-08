import numpy as np


a = np.array([[0,1,2],[3,4,5],[6,7,8]])
print("Dimension ",a.ndim)
print("Shape ",a.shape)
print("Content ",a[1,2])
print("Content ", a[1][2])
print("Size ", a.size)

print("=====================")
b = np.array([[0,1,2,9],[3,4,5,9],[6,7,8,9]])
print("Dimension ",b.ndim)
print("Shape ",b.shape)

X = np.array([[1, 0], [0, 1]]) 
Y = np.array([[2,3],[4,5]])
Z = X + Y
XX = X*Y
print(Z)
print(XX)

print("Matrix multiplication")
c = np.array([[1,1,1],[2,2,2]]) #2*3
d = np.array([[1,1],[2,2],[3,3]]) #3*2
e = np.dot(c,d)
print(e)

print("Transpose - " , e.T)

X=np.array([[1,0,1],[2,2,2]]) 
out=X[0:2,2]
print(out)

X=np.array([[1,0],[0,1]])
Y=np.array([[2,2],[2,2]])
Z=np.dot(X,Y)
print(Z)
