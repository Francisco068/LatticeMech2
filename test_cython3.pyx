import time
import random
import numba


def fill_random(L, c):
    x=[[None for i in range(c)] for j in range(L)]
    for i in range(L):
        for j in range(c):
            x[i][j]=random.random()
    return x


def f(x, y):
    for i in range(1000):
        for j in range(1000):
            x[i][j]=x[i][j]*y[0][j]
    return x

data1=fill_random(1000,1000)
data3=fill_random(1,1000)

t1=time.time()
data5=f(data1,data3)
t2=time.time()

print(t2-t1)
