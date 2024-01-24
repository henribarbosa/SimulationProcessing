from src.read_files import simulation_data

import numpy as np

class surface:
    def __init__(self, data: simulation_data):
        self.positions = data.build_time_series("positions").get_data()
        self.radius = data.build_time_series("radius").get_data()
        self.particle_classification = np.ones_like(data.types, dtype="uint8")

    def check_surface(self):
        print("Finding the surface...")
        for time in range(self.particle_classification.shape[0]):
            for check_particle in range(self.particle_classification.shape[1]):
                blocked_top = False
                blocked_side = False
                
                for test_particle in range(self.particle_classification.shape[1]):
                    
                    # test is the check particle
                    if test_particle == check_particle:
                        continue

                    # test is not in surface
                    if self.particle_classification[time][test_particle] == 0:
                        continue

                    # test is below check
                    belowY = self.positions[time][check_particle][1] < self.positions[time][test_particle][1] # Y_check < Y_test
                    belowZ = self.positions[time][check_particle][2] > self.positions[time][test_particle][2]
                    if belowY and belowZ:
                        continue 

                    blocked_Y = True
                    # test is not directly above check
                    max_dist = self.radius[time][check_particle] + self.radius[time][test_particle]
                    dist = np.sqrt(np.sum(np.square(self.positions[time][check_particle] - self.positions[time][test_particle]))-(self.positions[time][check_particle][1] - self.positions[time][test_particle][1])**2 )
                    if dist > max_dist:
                         blocked_Y = False

                    if (blocked_Y) and (not belowY):
                        blocked_side = True

                    blocked_Z = True
                    dist = np.sqrt(np.sum(np.square(self.positions[time][check_particle] - self.positions[time][test_particle]))-(self.positions[time][check_particle][2] - self.positions[time][test_particle][2])**2 )
                    if dist > max_dist:
                        blocked_Z = False

                    if (blocked_Z) and (not belowZ):
                        blocked_top = True

                if blocked_top and blocked_side:
                    self.particle_classification[time][check_particle] = 0

        return self

    def get_data(self):
        return self.particle_classification
