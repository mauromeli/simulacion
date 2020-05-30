# class Particle:
#
#     def __init__(self, x, y):
#         self.r = np.array((x, y))
#         self.radius = 0.5
#         self.right_movements = 0
#         self.left_movements = 0
#         self.up_movements = 0
#         self.down_movements = 0
#
#
#     @property
#     def x(self):
#         return self.r[0]
#
#     @x.setter
#     def x(self, value):
#         self.r[0] = value
#
#     @property
#     def y(self):
#         return self.r[1]
#
#     @y.setter
#     def y(self, value):
#         self.r[1] = value
#
#     def draw(self, ax):
#         circle = Circle(xy=self.r, radius=self.radius)
#         ax.add_patch(circle)
#         return circle
#
#     def out_of_boundery(self, step):
#         next_r = self.r + step
#
#         if next_r[0] + self.radius >= MAX_X or next_r[0] - self.radius < -MAX_X or next_r[1] + self.radius >= MAX_Y \
#                 or next_r[1] - self.radius < -MAX_Y:
#             return True
#         return False
#
#     def advance(self):
#         random_value = random.uniform(0, 1)
#         step = np.array((0, 0))
#
#         if random_value < 0.25:
#             step = np.array((1, 0))
#             self.up_movements += 1
#         elif random_value < 0.5:
#             step = np.array((0, -1))
#             self.down_movements += 1
#         elif random_value < 0.75:
#             step = np.array((-1, 0))
#             self.left_movements += 1
#         else:
#             step = np.array((0, 1))
#             self.right_movements += 1
#
#         if not self.out_of_boundery(step):
#             self.r += step
import random

from matplotlib import animation

from particle import Particle
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Simulation:

    ParticleClass = Particle

    def __init__(self, amount_of_circles=10, max_x=30, max_y=30, frames=100, fps=10):
        self.particles = []
        self.max_x = max_x
        self.max_y = max_y
        self.amount_of_circles = amount_of_circles
        self.init_particles(amount_of_circles)
        self.movements = 0
        self.frames = frames
        self.fps = fps

    def init_particles(self, amount_of_circles):
        for i in range(0, amount_of_circles):
            self.place_particle()

    def place_particle(self):
        x = random.randint(-self.max_x + 1, self.max_x - 1)
        y = random.randint(-self.max_y + 1, self.max_y - 1)

        particle = self.ParticleClass(x, y, self.max_x, self.max_y)
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
        # print("Movimiento", self.movements)
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