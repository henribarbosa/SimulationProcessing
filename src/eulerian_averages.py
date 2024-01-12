import numpy as np
from src.bed_points_array import points_array
from src.read_files import time_step_data, simulation_data

# Average the desired measument in the points of the bed
class eulerian_average:
    def __init__(self, lagrangian_data, points=points_array(0.0015,0.1)):
        self.points_coordinates = np.vstack((np.array(points.points_x),
                                             np.array(points.points_y),
                                             np.array(points.points_z))).T

        

        self.average_vector = np.zeros(points.n_total)


    def 
