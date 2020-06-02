from simulation import Simulation
import matplotlib.lines as lines

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
        count = {'right': {'blue': 0, 'red': 0}, 'left': {'blue': 0, 'red': 0}}

        for particle in self.particles:
            if particle.x < 0:
                count['left'][particle.color] += 1
            else:
                count['right'][particle.color] += 1

        self.densities['left']['blue'].append(count['left']['blue'] / self.area)
        self.densities['left']['red'].append(count['left']['red'] / self.area)
        self.densities['right']['blue'].append(count['right']['blue'] / self.area)
        self.densities['right']['red'].append(count['right']['red'] / self.area)

    def setup_animation(self):
        super().setup_animation()
        pointed_line = lines.Line2D([0, 0], [self.max_y, -self.max_y], lw=1,
                                    color='black', axes=self.ax, linestyle='--')
        self.ax.add_line(pointed_line)
        if self.wall:
            line = lines.Line2D([0, 0], [self.max_y, 0], lw=2, color='black', axes=self.ax)
            self.ax.add_line(line)