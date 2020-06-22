import numpy 
import time
cimport numpy

def f(numpy.ndarray x, numpy.ndarray y):
    cdef int taille=x.shape[1]
    for i in range(taille):
        x[i,:]=x[i,:]*y
    return x

data1=numpy.float32(numpy.random.random(1_000_000),dtype=numpy.float)
data3=numpy.float32(numpy.random.random(1000),dtype=numpy.float)
data4=numpy.float32(numpy.diag(data3),dtype=numpy.float)

data2=1000*data1
data2=numpy.reshape(data2,[1000,1000])
t1=time.time()
data5=f(data2,data3)
t2=time.time()

print(t2-t1)
