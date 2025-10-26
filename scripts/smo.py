import numpy as np
import matplotlib.pyplot as plt

class RobotPathPlanning:
    def __init__(self, start=(0, 0), end=(1000, 1000), scenario=None, number_obstacles=8):
        self.start = start
        self.end = end
        self.scenario = scenario if scenario is not None else self.generate_scenario(number_obstacles)
        self.path = None

    def generate_scenario(self, number_obstacles):
        return tuple((50 * np.random.randint(1, self.end[0]//50),
                      50 * np.random.randint(1, self.end[1]//50),
                      25 * np.random.randint(1, 9))
                     for _ in range(number_obstacles))

    def show_map(self):
        fig, ax = plt.subplots()
        for x, y, r in self.scenario:
            ax.add_patch(plt.Circle((x, y), r, color='blue', fill=False, linewidth=2))
        ax.plot(*self.start, 'go', markersize=8)
        ax.plot(*self.end, 'ro', markersize=8)
        if self.path:
            ax.plot(*zip(*self.path), linestyle='--', color='black')
        ax.set_xlim(self.start[0]-20, self.end[0]+20)
        ax.set_ylim(self.start[1]-20, self.end[1]+20)
        ax.set_aspect('equal')
        plt.show()

    def objective_function(self, alpha=1000):
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
        total_length = 0
        total_collisions = 0
        for p1, p2 in zip(self.path, self.path[1:]):
            total_length += np.linalg.norm(np.array(p2) - np.array(p1))
            for circle in self.scenario:
                total_collisions += count_collisions(p1, p2, circle)
        return total_length + alpha*total_collisions

    def generate_individual(self, path_size):
        individual = list((np.random.uniform(self.start[0], self.end[0]),
                           np.random.uniform(self.start[1], self.end[1]))
                          for _ in range(path_size))
        individual.insert(0, self.start)
        individual.append(self.end)
        return individual

    def path_smo(self, pop_size=10, max_iter=10, wait_iterations=10, max_r=10):
        strategy = "explotation"
        individuals = [self.generate_individual(2) for i in range(pop_size)]
        for i in range(max_iter):
            
            print()
        print(individuals)
        #etc

    def exploitation_smo(self, current_individual, n_neighbours, max_r):
        print()

    def exploration_smo(self):
        print()
        
    
    
        
p = RobotPathPlanning()
p.path_smo()


