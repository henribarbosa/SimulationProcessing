import numpy as np
from src.eulerian_averages import eulerian_average, sphere_intersection

def granular_temperature(eulerian_class):
    AVG_velocities = eulerian_class.make_vector_average("velocities").get_vector_data()

