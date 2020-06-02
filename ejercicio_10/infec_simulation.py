from simulation import Simulation
from infec_particles import infec_particles
import random
import matplotlib.animation as animation

class infec_simulation(Simulation):

    ParticleClass = infec_particles

    def __init__(self, amount_of_circles=10, max_x=30, max_y=30, frames=100, fps=10):
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
        self.infections_per_cicle = [5] #5 infected at timestamp 1 always

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

        if(color == "Red"):
            particle.time_infected +=1

        self.particles.append(particle)
        return True

    def do_animation(self, save=False, interval=1, filename='collision.gif'):
        self.setup_animation()
        anim = animation.FuncAnimation(self.fig, self.animate,
                                       init_func=self.init, frames=self.frames, interval=interval, blit=True)
        self.save_or_show_animation(anim, save, filename)

        return self.infections_per_cicle


    def advance_animation(self):
        for i, p in enumerate(self.particles):
            p.advance()
            self.circles[i].center = p.r

        #self.cure_particles(self.circles) #TO USE MODEL A COMMENT THIS LINE

        self.change_state(self.circles)
        self.count_infections(self.circles)

        return self.circles


    # Change the state of the particle, infected = red, not infected = blue, in each iteration
    def change_state(self, circles):

        for i in range(0, len(circles)):
            j = i + 1
            infected = False
            while not infected and (j < len(circles) -1):

                if (circles[i].get_facecolor() == (1.0, 0.0, 0.0, 1.0)): #Code of red color
                    neighbors = self.calclulate_neighbors(circles[i], circles[j])

                    if((neighbors)):
                        infect_prob = random.uniform(0,1)

                        if(infect_prob <= 0.6):
                            circles[j].set_facecolor("Red")
                            infected = True

                j = j + 1


    #Calculate the 8 posibilitys of being neighbors
    def calclulate_neighbors(self, circle1, circle2):

        option1 = (circle1.center[0] == circle2.center[0]) and (
                    circle1.center[1] + 1 == circle2.center[1] or circle1.center[1] - 1 == circle2.center[1])

        option2 = (circle1.center[1] == circle2.center[1]) and (
                    circle1.center[0] + 1 == circle2.center[1] or circle1.center[0] - 1 == circle2.center[1])

        option3 = (circle1.center[0] - 1 == circle2.center[0]) and (
                    circle1.center[1] + 1 == circle2.center[1] or circle1.center[1] - 1 == circle2.center[1])

        option4 = (circle1.center[0] + 1 == circle2.center[0]) and (
                    circle1.center[1] + 1 == circle2.center[1] or circle1.center[1] - 1 == circle2.center[1])

        if(option1 or option2 or option3 or option4):
            return True
        else:
            return False

    #Count the number of infections per cicle
    def count_infections(self, circles):

        number_of_infected = 0

        for i in range(0, len(circles)):

            if (circles[i].get_facecolor() == (1.0, 0.0, 0.0, 1.0)):
                number_of_infected = number_of_infected + 1
                self.particles[i].time_infected += 1

        self.infections_per_cicle.append(number_of_infected)


    #Cure the particles if it can be cure
    def cure_particles(self, circles):

        for i in range(0, len(self.particles)):

            if(self.particles[i].time_infected >= 20):

                prob_cure = random.uniform(0,3)

                if(prob_cure <= 0,1):
                    self.circles[i].set_facecolor("Blue")
                    self.particles[i].time_infected = 0