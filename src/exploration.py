import numpy as np

from generate import generate
from evaluate_fitness import evaluate_fitness

def exploration(x,max_R,p_end,p_back):
    class son:
        def __init__(self, individual, parent):
            self.individual = individual 
            self.parent = parent
    X=son(individual=x, parent=np.nan)
    X_init=X.individual
    R=np.random.uniform(0,max_R)
    new_sols=[X.individual]
    new_fits=[evaluate_fitness(X.individual)]
    path=[X.individual]
    path_fits=[evaluate_fitness(X.individual)]
    while True:
        X_1=son(individual=generate(X.individual,R), parent=X)
        ind=X_1.individual
        ind_fit=evaluate_fitness(ind)
        new_sols.append(ind)
        new_fits.append(ind_fit)
        path.append(ind)
        path_fits.append(ind_fit)
        X=X_1
        while np.random.rand()<p_back and X.parent!=np.nan:
            path.pop()
            path_fits.pop()
            X=X.parent
        if np.random.rand()<p_end:
            break
    
    fit_best=min(new_fits)
    X_best=new_sols[new_fits.index(fit_best)]

    return X_best,fit_best,path,path_fits
