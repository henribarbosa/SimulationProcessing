import numpy as np
from src.eulerian_averages import eulerian_average, sphere_intersection

def granular_temperature(eulerian_class):
    eulerian_class.change_radius(2*eulerian_class.radius)
    AVG_velocities = eulerian_class.make_vector_average("velocities").get_vector_data()

    eulerian_class.avg_quantity = "granular_temperature"
    data = eulerian_class.lagrangian_data.build_time_series("velocities").get_data()
    delta_velocity = np.zeros(AVG_velocities.shape)

    deltas = []
    for timeDataIndex in range(len(data)):
        eulerian_class.particle_volume = np.zeros([eulerian_class.number_points])
        delta_velocity = np.zeros([eulerian_class.number_points,3])
        for particleIndex in range(len(data[0])):
            particle_position = np.vstack(
             (np.ones(eulerian_class.number_points)*eulerian_class.positions[timeDataIndex][particleIndex][0],
              np.ones(eulerian_class.number_points)*eulerian_class.positions[timeDataIndex][particleIndex][1],
              np.ones(eulerian_class.number_points)*eulerian_class.positions[timeDataIndex][particleIndex][2])).T
            delta = eulerian_class.points_coordinates - particle_position
            delta = np.square(delta)
            delta = np.sum(delta, axis=1)
            delta = np.sqrt(delta) # distance between particle and point

            volume = sphere_intersection(delta, eulerian_class.radius, eulerian_class.lagrangian_data.radius[timeDataIndex][particleIndex])
            eulerian_class.particle_volume = eulerian_class.particle_volume + volume

            delta_velocity = delta_velocity + np.vstack([volume,volume,volume]).T * np.square( np.outer(data[timeDataIndex][particleIndex], np.ones(volume.shape)).T - AVG_velocities[timeDataIndex] )

        delta_velocity = 1/3 * np.sum(delta_velocity, axis=1)
        delta_velocity = np.divide(delta_velocity, eulerian_class.particle_volume, out=np.zeros_like(delta_velocity), where=eulerian_class.particle_volume!=0)

        deltas.append(delta_velocity)

    eulerian_class.change_radius(1/2*eulerian_class.radius)

    return np.array(deltas)
