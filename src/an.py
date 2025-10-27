import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
from scipy.stats import f_oneway, kruskal

# --- IMPORTA TU ALGORITMO, ESCENARIO Y FUNCIÓN DE FITNESS ---
from smo import smo_basic_loop
from obstacles import scenarios
from evaluate_fitness import evaluate_fitness

# Configuración inicial
scenario_name = "Scenario 1"
scenario = scenarios[scenario_name]
start_point = (0, 0)
end_point = (1000, 1000)


# --- Función auxiliar para obtener métricas de una ruta ---
def compute_metrics(path, scenario):
    """
    Calcula métricas clave de una ruta:
    - Longitud total
    - Número de colisiones
    - Fitness total penalizado
    """
    if path is None or len(path) == 0:
        return np.nan, np.nan, np.nan

    X = np.array(path).flatten()
    fitness_value = evaluate_fitness(X, scenario, alpha=1000)

    # Para obtener colisiones y longitud por separado
    # Repetimos la lógica interna de evaluate_fitness sin penalización
    total_length = 0
    total_collisions = 0

    auxiliar = [(0, 0)] + [tuple(X[i:i+2]) for i in range(0, len(X), 2)] + [(1000, 1000)]
    circles = [(scenario[f"c{i}"][0], scenario[f"c{i}"][1], scenario[f"r{i}"]) for i in range(1, len(scenario)//2 + 1)]

    def count_collisions(p1, p2, circle):
        p1, p2 = np.array(p1), np.array(p2)
        c, r = np.array(circle[:2]), circle[2]
        d = p2 - p1
        f = p1 - c
        a = np.dot(d, d)
        b = 2 * np.dot(f, d)
        c_term = np.dot(f, f) - r**2
        disc = b**2 - 4*a*c_term
        if disc < 0:
            return 0
        sqrt_disc = np.sqrt(disc)
        t1 = (-b - sqrt_disc) / (2*a)
        t2 = (-b + sqrt_disc) / (2*a)
        return int((0 <= t1 <= 1) or (0 <= t2 <= 1))

    for p1, p2 in zip(auxiliar, auxiliar[1:]):
        total_length += np.linalg.norm(np.array(p2) - np.array(p1))
        for circle in circles:
            total_collisions += count_collisions(p1, p2, circle)

    return fitness_value, total_length, total_collisions


# --- Experimentos automatizados ---
def run_experiments():
    pop_sizes = [10, 20, 40]
    max_iters = [200, 500]
    max_rs = [30, 40, 60]
    path_sizes = [2, 3]
    repetitions = 5

    results = []
    total_runs = len(pop_sizes) * len(max_iters) * len(max_rs) * len(path_sizes) * repetitions
    run_count = 0

    print(f"🚀 Iniciando {total_runs} ejecuciones experimentales...\n")

    for pop in pop_sizes:
        for iters in max_iters:
            for r in max_rs:
                for ps in path_sizes:
                    for rep in range(repetitions):
                        run_count += 1
                        print(f"▶️ Ejecución {run_count}/{total_runs}: pop={pop}, iter={iters}, r={r}, path={ps}, rep={rep+1}")

                        start_time = time.time()
                        best_path, evolution = smo_basic_loop(
                            pop_size=pop,
                            max_iter=iters,
                            wait_iterations=10,
                            max_r=r,
                            path_size=ps,
                            scenario=scenario,
                            n_neighbours=5
                        )
                        runtime = time.time() - start_time

                        fitness_value, path_length, n_collisions = compute_metrics(best_path, scenario)
                        iterations_used = len(evolution["best_fitness"])

                        results.append({
                            "pop_size": pop,
                            "max_iter": iters,
                            "max_r": r,
                            "path_size": ps,
                            "rep": rep + 1,
                            "fitness": fitness_value,
                            "path_length": path_length,
                            "collisions": n_collisions,
                            "iterations": iterations_used,
                            "runtime": runtime
                        })

    df = pd.DataFrame(results)
    df.to_csv("results_smo_with_fitness.csv", index=False)
    print("\n✅ Experimentos completados. Resultados guardados en 'results_smo_with_fitness.csv'\n")

    return df


# --- Análisis estadístico y visual ---
def analyze_results(df):
    print("📊 Análisis estadístico de los resultados\n")

    summary = df.groupby(["pop_size", "max_iter", "max_r", "path_size"]).agg(
        fitness_mean=("fitness", "mean"),
        fitness_std=("fitness", "std"),
        path_len_mean=("path_length", "mean"),
        path_len_std=("path_length", "std"),
        coll_mean=("collisions", "mean"),
        time_mean=("runtime", "mean"),
        iter_mean=("iterations", "mean")
    ).reset_index()

    print("Resumen estadístico por configuración:\n")
    print(summary.round(3).to_string(index=False))

    # --- ANOVA: efecto del tamaño de población sobre el fitness ---
    anova = f_oneway(*[group["fitness"].values for name, group in df.groupby("pop_size")])
    print("\n📈 ANOVA por tamaño de población:")
    print(f"F = {anova.statistic:.3f}, p = {anova.pvalue:.4f}")
    if anova.pvalue < 0.05:
        print("➡️ Diferencias significativas entre configuraciones de población (p < 0.05).")

    # --- Kruskal-Wallis: alternativa no paramétrica ---
    kruskal_test = kruskal(*[group["fitness"].values for name, group in df.groupby("pop_size")])
    print("\n📈 Kruskal-Wallis por tamaño de población:")
    print(f"H = {kruskal_test.statistic:.3f}, p = {kruskal_test.pvalue:.4f}")

    # --- Gráficos exploratorios ---
    sns.set(style="whitegrid")

    plt.figure(figsize=(7, 5))
    sns.boxplot(data=df, x="pop_size", y="fitness", palette="Set2")
    plt.title("Distribución del Fitness según Tamaño de Población")
    plt.xlabel("Tamaño de población")
    plt.ylabel("Fitness final")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(7, 5))
    sns.heatmap(
        df.pivot_table(values="fitness", index="pop_size", columns="max_iter", aggfunc="mean"),
        annot=True, fmt=".1f", cmap="coolwarm"
    )
    plt.title("Mapa de calor del fitness medio (pop_size vs max_iter)")
    plt.show()

    plt.figure(figsize=(7, 5))
    sns.barplot(data=summary, x="pop_size", y="coll_mean", hue="path_size", palette="viridis")
    plt.title("Promedio de colisiones según tamaño de población y complejidad de ruta")
    plt.ylabel("Colisiones promedio")
    plt.xlabel("Tamaño de población")
    plt.tight_layout()
    plt.show()

    return summary


# --- MAIN ---
if __name__ == "__main__":
    df_results = run_experiments()
    summary_table = analyze_results(df_results)
