import random
from particle import Particle
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Simulation:

    ParticleClass = Particle

    def __init__(self, amount_of_circles=10, max_x=30, max_y=30, frames=100, fps=10, wall=False, step_size=1):
        self.particles = []
        self.max_x = max_x
        self.max_y = max_y
        self.amount_of_circles = amount_of_circles
        self.init_particles(amount_of_circles)
        self.movements = 0
        self.frames = frames
        self.fps = fps
        self.left_density = []
        self.right_density = []
        self.area = self.max_x * self.max_y * 4
        self.wall = wall
        self.step_size = step_size


    def calculate_area(self):
        return self.max_x * self.max_y * 4

    def init_particles(self, amount_of_circles):
        for i in range(0, amount_of_circles):
            self.place_particle()

    def place_particle(self):
        x = random.randint(-self.max_x + 1, self.max_x - 1)
        y = random.randint(-self.max_y + 1, self.max_y - 1)

        particle = self.ParticleClass(x, y, self.max_x, self.max_y, self)
        self.particles.append(particle)
        return True

    def init(self):
        self.circles = []
        for particle in self.particles:
            self.circles.append(particle.draw(self.ax))
        return self.circles

    def do_animation(self, save=False, interval=1, filename='collision.gif'):
        self.setup_animation()
        anim = animation.FuncAnimation(self.fig, self.animate,
                                       init_func=self.init, frames=self.frames, interval=interval, blit=True)
        self.save_or_show_animation(anim, save, filename)

    def animate(self, i):
        self.advance_animation()
        self.movements += 1

        self.calculate_density()
        return self.circles

    def advance_animation(self):
        for i, p in enumerate(self.particles):
            p.advance()
            self.circles[i].center = p.r
        return self.circles

    def setup_animation(self):
        self.fig, self.ax = plt.subplots()
        for s in ['top', 'bottom', 'left', 'right']:
            self.ax.spines[s].set_linewidth(2)
        self.ax.set_aspect('equal', 'box')
        self.ax.set_xlim(-self.max_x, self.max_x)
        self.ax.set_ylim(-self.max_y, self.max_y)

    def save_or_show_animation(self, anim, save, filename='caminoparticula.gif', plt=None):
        if save:
            Writer = animation.writers['imagemagick']
            writer = Writer(fps=self.fps, bitrate=1800)
            anim.save(filename, writer=writer)
        else:
            plt.show()

    def calculate_density(self):
        count_left = 0
        count_right = 0
        for particle in self.particles:
            if particle.x < 0:
                count_left += 1
            else:
                count_right += 1

        left_density = count_left / self.area
        right_density = count_right / self.area

        self.left_density.append(left_density)
        self.right_density.append(right_density)

