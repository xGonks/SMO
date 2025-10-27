import matplotlib.pyplot as plt



scenario1 = {"c1": (300,150), "r1": 75,
             "c2": (250,600), "r2": 100,
             "c3": (600,100), "r3": 100,
             "c4": (500,750), "r4": 100,
             "c5": (850,550), "r5": 75,
             "c6": (450,300), "r6": 75,
             "c7": (750,350), "r7": 50,
             "c8": (700,800), "r8": 75,}

scenario2 = {"c1": (250,50), "r1": 150,
             "c2": (380,420), "r2": 150,
             "c3": (550,100), "r3": 150,
             "c4": (250,750), "r4": 200,
             "c5": (700,500), "r5": 100,
             "c6": (850,250), "r6": 200,
             "c7": (450,700), "r7": 150,
             "c8": (750,800), "r8": 150,}

scenario3 = {"c1": (200,200), "r1": 100,
             "c2": (380,500), "r2": 150,
             "c3": (550,150), "r3": 125,
             "c4": (250,750), "r4": 150,
             "c5": (750,450), "r5": 100,
             "c6": (800,250), "r6": 150,
             "c7": (500,700), "r7": 150,
             "c8": (800,800), "r8": 100,}

scenarios = {"Scenario 1": scenario1, "Scenario 2": scenario2, "Scenario 3": scenario3}



def plot_scenario(scenario, title="Scenario"):
    fig, ax = plt.subplots()
    ax.set_aspect(1)

    for i in range(1, 9):
        center = scenario[f"c{i}"]
        radius = scenario[f"r{i}"]
        circle = plt.Circle(center, radius, color='red', alpha=0.5)
        ax.add_artist(circle)

    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 1000)
    plt.title(title)
    plt.show()

