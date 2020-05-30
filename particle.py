from matplotlib.patches import Circle
import numpy as np
import random

# MAX_X = 30
# MAX_Y = 30
# PARTICLES_AMOUNT = 1
# FRAMES = 1000
# FPS = 100


class Particle:

    def __init__(self, x, y, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.radius = 0.5
        self.right_movements = 0
        self.left_movements = 0
        self.up_movements = 0
        self.down_movements = 0
        self.r = np.array((x, y))


    @property
    def x(self):
        return self.r[0]

    @x.setter
    def x(self, value):
        self.r[0] = value

    @property
    def y(self):
        return self.r[1]

    @y.setter
    def y(self, value):
        self.r[1] = value

    def draw(self, ax):
        circle = Circle(xy=self.r, radius=self.radius)
        ax.add_patch(circle)
        return circle

    def out_of_boundery(self, step):
        next_r = self.r + step

        if next_r[0] + self.radius >= self.max_x or next_r[0] - self.radius < -self.max_x or next_r[1] + self.radius >= self.max_y \
                or next_r[1] - self.radius < -self.max_y:
            return True
        return False

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
