import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
from matplotlib.patches import Circle

MAX_X = 30
MAX_Y = 30

class Particle:

    def __init__(self, x, y):

        self.r = np.array((x, y))
        self.styles = {'edgecolor': 'b', 'fill': None}
        self.radius = 0.5

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
        # square = Circle(xy=self.r, width=1, height=1)
        square = Circle(xy=self.r, radius=self.radius)
        algo = ax.add_patch(square)
        return square

    def out_of_boundery(self, step):
        next_r = self.r + step

        if next_r[0] + self.radius >= MAX_X or next_r[0] - self.radius < -MAX_X or next_r[1] + self.radius >= MAX_Y \
                or next_r[1] - self.radius < -MAX_Y:
            return True
        return False

    def advance(self):
        random_value = random.uniform(0, 1)
        step = np.array((0, 0))

        if random_value < 0.25:
            step = np.array((1, 0))
            # movements['right']+=1
        elif random_value < 0.5:
            step = np.array((0, -1))
            # movements['down']+=1
        elif random_value < 0.75:
            step = np.array((-1, 0))
            # movements['left']+=1
        else:
            step = np.array((0, 1))
            # movements['up']+=1

        if not self.out_of_boundery(step):
            self.r += step

class Simulation:

    ParticleClass = Particle

    def __init__(self, amount_of_squares):
        self.particles = []
        # self.squares = []
        self.init_particles(amount_of_squares)
        self.movements = 0


    def init_particles(self, amount_of_squares):
        for i in range(0, amount_of_squares):
            self.place_particle()

    def place_particle(self):
        x = random.randint(-MAX_X + 1, MAX_X - 1)
        y = random.randint(-MAX_Y + 1, MAX_Y - 1)

        particle = self.ParticleClass(x, y)
        # Check that the Particle doesn't overlap one that's already
        # been placed.
        self.particles.append(particle)
        return True

    def init(self):
        """Initialize the Matplotlib animation."""
        print('entre a init')
        self.squares = []
        for particle in self.particles:
            self.squares.append(particle.draw(self.ax))
        return self.squares

    def do_animation(self, save=False, interval=1, filename='collision.gif'):
        """Set up and carry out the animation of the molecular dynamics.

        To save the animation as a MP4 movie, set save=True.
        """

        self.setup_animation()
        anim = animation.FuncAnimation(self.fig, self.animate,
                                       init_func=self.init, frames=100, interval=interval, blit=True)
        self.save_or_show_animation(anim, save, filename)

    def animate(self, i):
        """The function passed to Matplotlib's FuncAnimation routine."""
        # print([square.center for square in self.squares])
        self.movements += 1
        print(self.movements)
        self.advance_animation()

        return self.squares

    def advance_animation(self):
        """Advance the animation by dt, returning the updated Circles list."""

        for i, p in enumerate(self.particles):
            p.advance()
            # self.squares[i].set_xy(p.r)
            self.squares[i].center = p.r
        return self.squares


    def setup_animation(self):
        self.fig, self.ax = plt.subplots()
        for s in ['top', 'bottom', 'left', 'right']:
            self.ax.spines[s].set_linewidth(2)
        self.ax.set_aspect('equal', 'box')
        self.ax.set_xlim(-MAX_X, MAX_X)
        self.ax.set_ylim(-MAX_Y, MAX_Y)
        # self.ax.xaxis.set_ticks([])
        # self.ax.yaxis.set_ticks([])

    def save_or_show_animation(self, anim, save, filename='collision.gif'):
        if save:
            Writer = animation.writers['imagemagick']
            writer = Writer(fps=10, bitrate=1800)
            anim.save(filename, writer=writer)
        else:
            plt.show()

if __name__ == '__main__':
    nparticles = 10
    sim = Simulation(nparticles)
    sim.do_animation(save=True)


