import numpy as np
import matplotlib.pyplot as plt

from smo import smo_basic_loop
from obstacles import scenarios

scenario_name = "Scenario 1"
scenario = scenarios[scenario_name]

start_point = (0, 0)
end_point = (1000, 1000)

def draw_environment(ax, scenario_dict, path=None, title="Robot Path Planning"):
    """Dibuja el mapa, obstáculos y una ruta opcional."""
    ax.clear()
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 1000)
    ax.set_aspect('equal')
    ax.set_title(title, fontsize=11)

    ax.plot(*start_point, 'go', markersize=10, label="Inicio")
    ax.plot(*end_point, 'ro', markersize=10, label="Meta")

    for i in range(1, 9):
        center = scenario_dict[f"c{i}"]
        radius = scenario_dict[f"r{i}"]
        circle = plt.Circle(center, radius, color='blue', fill=False, linewidth=2)
        ax.add_patch(circle)

    if path is not None:
        path_array = np.array(path).reshape(-1, 2)
        
        full_path = np.vstack([start_point, path_array, end_point])
        ax.plot(full_path[:, 0], full_path[:, 1], '--k', lw=2, label="Ruta actual")
        ax.plot(full_path[:, 0], full_path[:, 1], 'ok', markersize=3)  # Puntos pequeños

    ax.legend(loc='upper left')

def run_smo_visualization():
    print("Ejecutando Slime Mould Optimizer (SMO) para planificación de rutas...\n")

    pop_size = 20
    max_iter = 500
    wait_iterations = 10
    max_r = 40
    path_size = 2

    best_path, evolution = smo_basic_loop(
        pop_size=pop_size,
        max_iter=max_iter,
        wait_iterations=wait_iterations,
        max_r=max_r,
        path_size=path_size,
        scenario=scenario,
        n_neighbours=5
    )

    plt.ion()
    fig, ax = plt.subplots(figsize=(6, 6))

    print("\nMostrando evolución de las soluciones...\n")

    step = max(1, len(evolution["best_paths"]) // 10)
    for i in range(0, len(evolution["best_paths"]), step):
        path = evolution["best_paths"][i]
        fitness = evolution["best_fitness"][i]
        draw_environment(ax, scenario, path, title=f"Iteración {i+1} | Fitness: {fitness:.2f}")
        plt.pause(0.5)

    plt.ioff()

    fig2, ax2 = plt.subplots(figsize=(6, 6))
    draw_environment(ax2, scenario, best_path, title="Ruta óptima final")
    plt.show()

    plt.figure(figsize=(6, 4))
    plt.plot(evolution["best_fitness"], '-o', label="Best Fitness")
    plt.title("Evolución del mejor fitness")
    plt.xlabel("Iteración")
    plt.ylabel("Fitness (distancia penalizada)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    print("\n✅ Optimización completada.")
    print(f"Mejor fitness final: {evolution['best_fitness'][-1]:.4f}")
    print(f"Total de iteraciones: {len(evolution['best_fitness'])}")

if __name__ == "__main__":
    run_smo_visualization()
