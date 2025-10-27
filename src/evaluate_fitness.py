import numpy as np

def count_collisions(p1, p2, circle):
    p1, p2 = np.array(p1, dtype=float), np.array(p2, dtype=float)
    c, r = np.array(circle[:2], dtype=float), circle[2]
    d = p2 - p1
    f = p1 - c
    a = np.dot(d, d)
    b = 2 * np.dot(f, d)
    c_term = np.dot(f, f) - r**2
    discriminant = b**2 - 4*a*c_term
    if discriminant < 0:
        return 0
    elif discriminant == 0:
        t = -b / (2*a)
        return 1 if 0 <= t <= 1 else 0
    else:
        sqrt_disc = np.sqrt(discriminant)
        t1 = (-b - sqrt_disc) / (2*a)
        t2 = (-b + sqrt_disc) / (2*a)
        count = 0
        if 0 <= t1 <= 1: count += 1
        if 0 <= t2 <= 1: count += 1
        return count

def evaluate_fitness(X, scenario, alpha=1000):
    total_length = 0
    total_collisions = 0
    auxiliar = []
    auxiliar.append((0, 0))
    for i in range(0, len(X), 2):
        auxiliar.append((X[i], X[i+1]))
    auxiliar.append((1000, 1000))
    circles = []
    n = len(scenario) // 2
    for i in range(1, n + 1):
        cx, cy = scenario[f"c{i}"]
        r = scenario[f"r{i}"]
        circles.append((cx, cy, r))
    for p1, p2 in zip(auxiliar, auxiliar[1:]):
        total_length += np.linalg.norm(np.array(p2) - np.array(p1))
        for circle in circles:
            total_collisions += count_collisions(p1, p2, circle)
    return total_length + alpha * total_collisions