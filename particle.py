from matplotlib.patches import Circle
import numpy as np
import random

class Particle:

    def __init__(self, x, y, max_x, max_y, simulation):
        self.max_x = max_x
        self.max_y = max_y
        self.radius = 0.1
        self.right_movements = 0
        self.left_movements = 0
        self.up_movements = 0
        self.down_movements = 0
        self.r = np.array((x, y))
        self.simulation = simulation
        self.circle = None

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
        self.circle = circle
        ax.add_patch(circle)
        return circle

    def out_of_boundery(self, step):
        next_r = self.r + step

        # TODO: Queda horrible pero quizas funciona.
        if self.simulation.wall and ((self.r[0] <= 0 <= next_r[0] or self.r[0] >= 0 >= next_r[0])
                                     and (self.r[1] >= 0 or next_r[1] >= 0)):
            return True

        if next_r[0] + self.radius >= self.max_x or \
                next_r[0] - self.radius < -self.max_x or \
                next_r[1] + self.radius >= self.max_y or \
                next_r[1] - self.radius < -self.max_y:
            return True
        return False

    def advance(self):
        random_value = random.uniform(0, 1)
        step = np.array((0, 0))

        if random_value < 0.25:
            step = np.array((self.simulation.step_size, 0))
            self.up_movements += 1
        elif random_value < 0.5:
            step = np.array((0, -self.simulation.step_size))
            self.down_movements += 1
        elif random_value < 0.75:
            step = np.array((-self.simulation.step_size, 0))
            self.left_movements += 1
        else:
            step = np.array((0, self.simulation.step_size))
            self.right_movements += 1

        if not self.out_of_boundery(step):
            self.r += step
