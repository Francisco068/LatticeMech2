import numpy as np 
import time

def MatMulVect(x,y,r):
    """Multiply a 2D square np.array x and a diagonal matrix y 
    y wrote as a 1D np.array, r=result
    """
    taille=x.shape[1]

    for i in range(taille):
        r[i,:]=x[i,:]*y
    return r

data1=np.array([i for i in range(16) ],dtype=float)
data3=np.array([i for i in range(4)],dtype=float)

data1=np.reshape(data1,[4,4])
t=np.copy(data1)
t1=time.time()

MatMulVect(data1,data3,t)
t2=time.time()

print((t2-t1))
