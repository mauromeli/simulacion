from simulation import Simulation
from infec_particles import infec_particles
import random
import matplotlib.animation as animation

class infec_simulation(Simulation):

    ParticleClass = infec_particles

    def __init__(self, amount_of_circles=10, max_x=30, max_y=30, frames=100, fps=10, model = "A", type_of_moving = 1):
        self.particles = []
        self.max_x = max_x
        self.max_y = max_y
        self.amount_of_circles = amount_of_circles
        self.model = model
        self.type_of_moving = type_of_moving
        self.init_particles(amount_of_circles)
        self.movements = 0
        self.fps = fps
        self.left_density = []
        self.right_density = []
        self.area = self.max_x * self.max_y * 4
        self.infections_per_cicle = []
        self.frames = frames


    def init_particles(self, amount_of_circles):
        inicial_infected_particles = 0
        moving_particles = amount_of_circles
        for i in range(0, amount_of_circles):
            color = "Blue"
            can_move = 1

            if (inicial_infected_particles < 5): #95% of the particles began infected
                number = random.uniform(0,1)

                if (number < 0.5): #50% of probability to began infected
                    color = "Red"
                    inicial_infected_particles += 1

            if(self.type_of_moving == 3):  # only 50% of the particles can move
                if (moving_particles >= (amount_of_circles / 2)):
                    can_move = 0
                    moving_particles -= 1

            if (self.type_of_moving == 2 and color == "Red"): #Only healthy particles can move
                can_move = 0

            self.place_particle(color, can_move)

    def init(self):
        self.circles = []
        for particle in self.particles:
            self.circles.append(particle.draw(self.ax))
        return self.circles

    def place_particle(self, color, can_move):
        x = random.randint(-self.max_x + 1, self.max_x - 1)
        y = random.randint(-self.max_y + 1, self.max_y - 1)

        particle = self.ParticleClass(x, y, self.max_x, self.max_y, color, can_move)

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

            if(p.can_move == 1):
                p.advance()

            self.circles[i].center = p.r

        if(self.model == "B"):
            self.cure_particles(self.circles)

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

    #Count the number of infections per cicle and stop them if type of moving is 2
    def count_infections(self, circles):

        number_of_infected = 0

        for i in range(0, len(circles)):

            if (circles[i].get_facecolor() == (1.0, 0.0, 0.0, 1.0)):
                number_of_infected = number_of_infected + 1
                self.particles[i].time_infected += 1

                if(self.type_of_moving == 2): #Only healthy particles can move

                    if (self.particles[i].time_infected >= 10 or self.particles[i].time_infected <= 20):

                        prob_to_stop = random.uniform(0,1)

                        if(prob_to_stop <= 0,5):
                            self.particles[i].can_move = 0

                    if (self.particles[i].time_infected > 20):
                        self.particles[i].can_move = 0

        self.infections_per_cicle.append(number_of_infected)


    #Cure the particles if it can be cure and let them move if type moving is 2
    def cure_particles(self, circles):

        for i in range(0, len(self.particles)):

            if(self.particles[i].time_infected >= 20):

                prob_cure = random.uniform(0,1)

                if(prob_cure <= 0,8):
                    self.circles[i].set_facecolor("Blue")
                    self.particles[i].time_infected = 0

                    if(self.type_of_moving == 2): #Only healthy particles can move
                        self.particles[i].can_move = 1
