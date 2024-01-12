import numpy as np
from bed_points_array import points_array
from read_files import time_step_data, simulation_data

# Average the desired measument in the points of the bed
class eulerian_average:
    def __init__(self, lagrangian_data, points=points_array(0.0015,0.1)):
        
    
