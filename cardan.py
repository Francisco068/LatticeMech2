# Cardan
import numpy as np
def SolveX3(c,d):
    delta=np.power(d,2)+4/27*np.power(c,3)
    u=(-d-np.sqrt(delta))/2
    v=(-d+np.sqrt(delta))/2
    if u<0:
        ru=-np.power(-u,1/3)
    else:
        ru=np.power(u,1/3)
    if v<0:
        rv=-np.power(-v,1/3)
    else:
        rv=np.power(v,1/3)
    x=ru+rv
    return x

x=SolveX3(10,15)
S=np.power(x,3)+10*x+15
print(S)