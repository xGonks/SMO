import numpy as np
import matplotlib.pyplot as plt

from evaluate_fitness import evaluate_fitness
from exploitation import exploitation
from exploration import exploration

def smo_basic_loop(pop_size=20, max_iter=50, wait_iterations=10, max_r=50, path_size=4, scenario=None, n_neighbours=5):
    strategy = "exploitation"
    population = [np.random.uniform(0, 1000, size=2*path_size) for _ in range(pop_size)]
    cardinalities = [1 for _ in range(pop_size)]
    fitness = [evaluate_fitness(ind, scenario) for ind in population]
    best_fitness = min(fitness)
    best_path = population[np.argmin(fitness)]
    stagnation_counter = 0

    # 🧠 Guardar progreso
    evolution = {
        "best_paths": [],
        "best_fitness": [],
        "all_population": [],
        "all_fitness": []
    }
    
    best_fitness_history = []

    for iter in range(max_iter):
        if stagnation_counter >= wait_iterations:
            strategy = "exploration" if strategy == "exploitation" else "exploitation"
            stagnation_counter = 0

        inv_fitness = 1 / (np.array(fitness) + 1e-9)
        probs = inv_fitness / np.sum(inv_fitness)
        selected_idx = np.random.choice(range(pop_size), p=probs)
        selected = population[selected_idx]

        # Ejecutar estrategia
        if strategy == "exploitation":
            best_fitness_history.append(best_fitness)
            n_neighbours = cardinalities[selected_idx]
            new_individuals, new_fits, new_cardinality, path, path_fits = exploitation(
                                                X=selected,
                                                n=n_neighbours,
                                                max_r=max_r,
                                                iter=iter,
                                                fits=best_fitness,
                                                C_X=10,
                                                scenario=scenario,
                                                all_fits=best_fitness_history  # ✅ historial de mejores fitness
                                            )

        else:
            X_best, fit_best, path, path_fits = exploration(x=selected, max_R=500,
                                                            p_end=0.3, p_back=0.1,
                                                            scenario=scenario)
            new_individuals = [X_best]
            new_fits = [fit_best]


        combined = population + new_individuals
        combined_fitness = fitness + new_fits
        best_idx = np.argsort(combined_fitness)[:pop_size]
        population = [combined[i] for i in best_idx]
        fitness = [combined_fitness[i] for i in best_idx]

        # Actualizar cardinalidades
        f_max, f_min = max(fitness), min(fitness)
        epsilon, k = 1e-9, 10
        cardinalities = [int(np.round(k * (f_max - f_i) / (f_max - f_min + epsilon))) + 1
                         for f_i in fitness]

        if min(fitness) < best_fitness:
            best_fitness = min(fitness)
            best_path = population[np.argmin(fitness)]
            stagnation_counter = 0
        else:
            stagnation_counter += 1

        # 🟢 Guardar progreso en memoria
        evolution["best_paths"].append(best_path)
        evolution["best_fitness"].append(best_fitness)
        evolution["all_population"].append(population.copy())
        evolution["all_fitness"].append(fitness.copy())

        print(f"Iter {iter+1}/{max_iter} | Best fitness: {best_fitness:.2f} | Strategy: {strategy}")

    # 🟢 Devolver el mejor resultado y la evolución completa
    return best_path, evolution
