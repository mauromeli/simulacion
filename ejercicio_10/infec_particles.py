from particle import Particle
from matplotlib.patches import Circle
import numpy as np
import random

class infec_particles(Particle):

    def __init__(self, x, y, max_x, max_y, color):
        self.color = color
        self.max_x = max_x
        self.max_y = max_y
        self.radius = 0.5
        self.right_movements = 0
        self.left_movements = 0
        self.up_movements = 0
        self.down_movements = 0
        self.r = np.array((x, y))
        self.time_infected = 0

    def draw(self, ax):
        circle = Circle(xy=self.r, radius=self.radius, facecolor=self.color)
        ax.add_patch(circle)
        return circle

    def advance(self):
        random_value = random.uniform(0, 1)
        step = np.array((0, 0))

        if random_value < 0.25:
            step = np.array((1, 0))
            self.up_movements += 1
        elif random_value < 0.5:
            step = np.array((0, -1))
            self.down_movements += 1
        elif random_value < 0.75:
            step = np.array((-1, 0))
            self.left_movements += 1
        else:
            step = np.array((0, 1))
            self.right_movements += 1

        if not self.out_of_boundery(step):
            self.r += step
