import numpy as np
import matplotlib.pyplot as plt

from evaluate_fitness import evaluate_fitness
from exploitation import exploitation
from exploration import exploration

def smo_basic_loop(pop_size=20, max_iter=50, wait_iterations=10, max_r=50, path_size=4, scenario=None, n_neighbours=5): # alpha=1000
    strategy = "exploitation"
    population = [np.random.uniform(0, 1000, size=2*path_size) for _ in range(pop_size)]
    fitness = [evaluate_fitness(ind, scenario) for ind in population]
    best_fitness = min(fitness)
    best_path = population[np.argmin(fitness)]

    stagnation_counter = 0

    for iter in range(max_iter):
        if stagnation_counter >= wait_iterations:
            strategy = "exploration" if strategy == "exploitation" else "exploitation"
            stagnation_counter = 0

        inv_fitness = 1 / (np.array(fitness)) # + 1e-9
        probs = inv_fitness / np.sum(inv_fitness)
        selected_idx = np.random.choice(range(pop_size), p=probs)
        selected = population[selected_idx]

        # Ejecutar estrategia
        if strategy == "exploitation":
            new_individuals = exploitation(X=selected, n=n_neighbours, max_r=max_r,
                                           iter=iter, fits=evaluate_fitness(selected, scenario), C_X=3)
        else:
            new_individuals = exploration(x=selected, max_R=500, p_end=0.3, p_back=0.1)

        new_fitness = [evaluate_fitness(ind, scenario) for ind in new_individuals]

        combined = population + new_individuals
        combined_fitness = fitness + new_fitness
        best_idx = np.argsort(combined_fitness)[:pop_size]
        population = [combined[i] for i in best_idx]
        fitness = [combined_fitness[i] for i in best_idx]
        
        if min(fitness) < best_fitness:
            best_fitness = min(fitness)
            best_path = population[np.argmin(fitness)]
            stagnation_counter = 0
        else:
            stagnation_counter += 1

        print(f"Iter {iter+1}/{max_iter} | Best fitness: {best_fitness:.2f} | Strategy: {strategy}")

    return best_path