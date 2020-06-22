import numba

import random 
import numpy as np
import time

data=np.random.random(1_000_000)

def carre(a):
    r=len(a)
    t=np.empty(r)
    t=np.cos(3*a)

t1=time.time()
carre(data)
t2=time.time()

print(t2-t1)