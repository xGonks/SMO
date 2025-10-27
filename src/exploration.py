import numpy as np

from generate import generate

def exploration(x,max_R,p_end,p_back):
    class son:
        def __init__(self, individual, parent):
            self.individual = individual 
            self.parent = parent
    X=son(individual=x, parent=np.nan)
    new_sols=[X.individual]
    X_init=X.individual
    R=np.random.uniform(0,max_R)
    path=[X.individual]
    while True:
        X_1=son(individual=generate(X.individual,R), parent=X)
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
    return new_sols,path

x=np.array([3.5,3.0])
sols,path=exploration(x,1.0,0.2,0.2)