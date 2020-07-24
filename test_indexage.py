# test adressage indexé python
a=[5]
b=[6]
c=[a,b]
print(a)
print(c)
a[0]=1

class variable():
    def __init__(self,type_var : str='t',index_var : int=0,ref : float=0.0):
        self.type_var=type_var
        self.index_var=index_var
        self.ref=ref

def GenereListe(n : int=1):
    L=[]
    for i in range(n):
        L.append([])