from src.read_files import simulation_data

import numpy as np

class surface:
    def __init__(self, data: simulation_data):
        self.positions = data.build_time_series("positions").get_data()
        self.particle_classification = np.ones_like(data.types)

    def check_surface(self):
        for time in range(self.particle_classification.shape[0]):
            for check_particle in range(self.particle_classification.shape[1]):
                for test_particle in range(self.particle_classification.shape[1]):
                    if self.particle_classification[time][test_particle] == 0:
                        continue

