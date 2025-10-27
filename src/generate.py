import numpy as np
import math as mt

def generate(x,r):
    v=np.zeros(len(x))
    k=0
    for i in range(len(v)):
        prob=1/mt.factorial(k)
        u=np.random.rand()
        if u<=prob:
            v[i]=1
            k+=1
    V=np.random.permutation(v)
    U=np.random.rand(len(x))
    x_1=x+V*(U*2*r-r)
    return x_1
