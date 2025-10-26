import numpy as np
import math as mt

def generate(X,r):
    v=np.zeros(len(X))
    k=0
    for item in v:
        prob=1/mt.factorial(k)
        u=np.random.rand()
        if u<=prob:
            item=1
            k+=1
    V=np.random.permutation(v)
    U=np.random.rand(len(X))
    X_1=X+V*(U*2*r-r)
    return X_1

def exploration(X,max_R,p_end,p_back):
    class son:
        def _init_(self, individual, parent):
            self.individual = individual 
            self.parent = parent
    X=son(X, np.nan)
    new_sols=[X.individual]
    X_init=X.individual
    R=np.random.uniform(max_R)
    path=[X.individual]
    while True:
        X_1=son(generate(X.individual,R), X)
        new_sols.append(X_1.individual)
        path.append(X_1.individual)
        X=X_1
        while np.random.rand()<p_back and X.parent!=np.nan:
            path.pop()
            X=X.parent
        if np.random.rand()<p_end:
            break
        #Evaluate
        #X_best=X_best.indivual (np array)
    return X_best