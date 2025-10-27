import numpy as np
from generate import generate
from evaluate_fitness import evaluate_fitness

def exploration(x, max_R, p_end, p_back, scenario):
    class Son:
        def __init__(self, individual, parent):
            self.individual = individual 
            self.parent = parent
    X = Son(individual=x, parent=None)
    R = np.random.uniform(0, max_R)
    new_sols = [X.individual]
    f_init = evaluate_fitness(X.individual, scenario)
    new_fits = [f_init]
    path = [X.individual]
    path_fits = [f_init]
    
    while True:
        X_1 = Son(individual=generate(X.individual, R), parent=X)
        ind = X_1.individual
        ind_fit = evaluate_fitness(ind, scenario)
        new_sols.append(ind)
        new_fits.append(ind_fit)
        path.append(ind)
        path_fits.append(ind_fit)
        X = X_1
        
        while np.random.rand() < p_back and X.parent is not None:
            path.pop()
            path_fits.pop()
            X = X.parent

        if np.random.rand() < p_end:
            break
        
    fit_best = min(new_fits)
    X_best = new_sols[new_fits.index(fit_best)]
    return X_best, fit_best, path, path_fits
