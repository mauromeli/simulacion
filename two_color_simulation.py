from simulation import Simulation
import matplotlib.lines as lines
import numpy as np

class TwoColorSimulation(Simulation):
    def __init__(self, amount_of_circles=10, max_x=30, max_y=30, frames=100, fps=10, wall=True, step_size=1):
        self.densities = {'right': {'blue': [], 'red': []}, 'left': {'blue': [], 'red': []}}
        super().__init__(amount_of_circles, max_x, max_y, frames, fps, wall, step_size)

    def init_particles(self, amount_of_circles):
        for i in range(0, int(amount_of_circles / 2)):
            self.place_particle(-self.max_x, 0, -self.max_y, self.max_y, 'blue')
        for i in range(int(amount_of_circles / 2), amount_of_circles):
            self.place_particle(0, self.max_x, -self.max_y, self.max_y, 'red')

    def calculate_density(self):
        self.densities['left']['blue'].append(self.count['left']['blue'] / self.area)
        self.densities['left']['red'].append(self.count['left']['red'] / self.area)
        self.densities['right']['blue'].append(self.count['right']['blue'] / self.area)
        self.densities['right']['red'].append(self.count['right']['red'] / self.area)

    def setup_animation(self):
        super().setup_animation()
        pointed_line = lines.Line2D([0, 0], [self.max_y, -self.max_y], lw=1,
                                    color='black', axes=self.ax, linestyle='--')
        self.ax.add_line(pointed_line)
        if self.wall:
            line = lines.Line2D([0, 0], [self.max_y, 0], lw=2, color='black', axes=self.ax)
            self.ax.add_line(line)

    def advance_animation(self):
        randoms = np.random.uniform(0, 1, self.amount_of_circles)

        for i, p in enumerate(self.particles):
            p.advance(randoms[i])
            self.circles[i].center = p.r

            if p.x < 0:
                self.count['left'][p.color] += 1
            else:
                self.count['right'][p.color] += 1

        return self.circles

    def animate(self, i):
        self.count = {'right': {'blue': 0, 'red': 0}, 'left': {'blue': 0, 'red': 0}}
        self.advance_animation()
        self.movements += 1
        print(self.movements)

        self.calculate_density()
        self.count = {'right': {'blue': 0, 'red': 0}, 'left': {'blue': 0, 'red': 0}}

        return self.circles