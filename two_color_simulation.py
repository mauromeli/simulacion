from simulation import Simulation

class TwoColorSimulation(Simulation):
    pass

    def init_particles(self, amount_of_circles):
        for i in range(0, int(amount_of_circles / 2)):
            self.place_particle(-self.max_x, 0, -self.max_y, self.max_y, 'blue')
        for i in range(int(amount_of_circles / 2), amount_of_circles):
            self.place_particle(0, self.max_x, -self.max_y, self.max_y, 'red')
