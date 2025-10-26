import numpy as np
def generate(X,r):
    v=np.zeros(len(X))
    k=0
    for item in v:
        prob=1/mt.factorial(k)
        u=np.random.rand()
        if u<=prob:
            item=1
            k+=1
    V=np.random.permutation()
    U=np.random.rand(len(X))
    X_1=X+V*(U*2*r-r)
    return X_1