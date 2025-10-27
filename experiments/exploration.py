import numpy as np

from generate import generate
from evaluate_fitness import evaluate_fitness

def nearest_state(fitness_value, Q):
    if not Q:
        return None        
    return min(Q.keys(), key=lambda f: abs(f - fitness_value))

def exploration(x, max_R, p_end, p_back, scenario, alpha=0.1, gamma=0.4, epsilon=0.1):
    class Son:
        def __init__(self, individual, parent):
            self.individual = individual
            self.parent = parent

    X = Son(individual=x, parent=np.nan)
    R = np.random.uniform(0, max_R)

    new_sols = [X.individual]
    new_fits = [evaluate_fitness(X.individual,scenario)]
    path = [X.individual]
    path_fits = [evaluate_fitness(X.individual,scenario)]

    Q = {}
    state = evaluate_fitness(X.individual,scenario)

    while True:
        if state not in Q:
            Q[state] = [0.0, 0.0]

        if np.random.rand() < epsilon:
            action = np.random.choice([0, 1])  # 0=back, 1=forward
        else:
            action = np.argmax(Q[state])

        if action == 1:  # forward
            X_1 = Son(individual=generate(X.individual, R), parent=X)
            next_ind = X_1.individual
            next_fit = evaluate_fitness(next_ind,scenario)
            X = X_1
            path.append(next_ind)
            path_fits.append(next_fit)
        else:  # back
            if isinstance(X.parent, Son):
                X = X.parent
                if path:
                    path.pop()
                    path_fits.pop()
            next_fit = evaluate_fitness(X.individual,scenario)

        reward = (state - next_fit)

        next_state = next_fit
        if next_state not in Q:
            nearest = nearest_state(next_state, Q)
            Q[next_state] = Q[nearest][:] if nearest is not None else [0.0, 0.0]

        Q[state][action] += alpha * (
            reward + gamma * np.max(Q[next_state]) - Q[state][action]
        )

        state = next_state
        new_sols.append(X.individual)
        new_fits.append(state)

        if np.random.rand() < p_end:
            break

    fit_best = min(new_fits)
    X_best = new_sols[new_fits.index(fit_best)]
    return X_best, fit_best, path, path_fits

