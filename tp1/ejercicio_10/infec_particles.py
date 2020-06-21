from particle import Particle
from matplotlib.patches import Circle
import numpy as np
import random

class infec_particles(Particle):

    def __init__(self, x, y, max_x, max_y, color, can_move = 1):
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
        self.can_move = can_move

    def draw(self, ax):
        circle = Circle(xy=self.r, radius=self.radius, facecolor=self.color)
        ax.add_patch(circle)
        return circle