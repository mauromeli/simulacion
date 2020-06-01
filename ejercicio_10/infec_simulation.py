from simulation import Simulation
from infec_particles import infec_particles
import random

class infec_simulation(Simulation):

    ParticleClass = infec_particles

    def init_particles(self, amount_of_circles):
        inicial_infected_particles = 0
        for i in range(0, amount_of_circles):

            if (inicial_infected_particles < 5): #95% of the particles began infected
                number = random.uniform(0,1)
                if (number < 0.5): #50% of probability to began infected
                    self.place_particle("Red")
                    inicial_infected_particles += 1
            else:
                self.place_particle("Blue")

    def init(self):
        self.circles = []
        for particle in self.particles:
            self.circles.append(particle.draw(self.ax))
        return self.circles

    def place_particle(self, color):
        x = random.randint(-self.max_x + 1, self.max_x - 1)
        y = random.randint(-self.max_y + 1, self.max_y - 1)

        particle = self.ParticleClass(x, y, self.max_x, self.max_y, color)

        if(color == 'r'):
            particle.time_infected +=1

        self.particles.append(particle)
        return True


    def advance_animation(self):
        for i, p in enumerate(self.particles):
            p.advance()
            self.circles[i].center = p.r

        self.change_state(self.circles)

        return self.circles


    # Change the state of the particle, infected = red, not infected = blue, in each iteration
    def change_state(self, circles):

        for i in range(0, len(circles)):
            j = i + 1
            infected = False
            while not infected and (j < len(circles) -1):

                if (circles[j].get_facecolor() != circles[i].get_facecolor()):
                    neighborX = circles[i].center[0] + 1 == circles[j].center[0] or circles[i].center[0] - 1 == circles[j].center[0]
                    neighborY = circles[i].center[1] + 1 == circles[j].center[1] or circles[i].center[1] - 1 == circles[j].center[1]

                    if((neighborX or neighborY)):
                        infect_prob = random.uniform(0,1)

                        if(infect_prob < 0.9):
                            circles[i].set_facecolor("Red")
                            infected = True

                j += 1