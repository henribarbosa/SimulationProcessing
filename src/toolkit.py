import numpy as np
from src.eulerian_averages import eulerian_average, sphere_intersection

def granular_temperature(eulerian_class: eulerian_average):
    eulerian_class.change_radius(5*eulerian_class.radius)
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

    eulerian_class.change_radius(1/5*eulerian_class.radius)

    return np.array(deltas)

def packing_fraction(eulerian_class: eulerian_average):
    data = eulerian_class.lagrangian_data.build_time_series("positions").get_data()

    pfractions = []
    for timeDataIndex in range(len(data)):
        eulerian_class.particle_volume = np.zeros([eulerian_class.number_points])
        measurement_volume = np.zeros([eulerian_class.number_points])

        d = eulerian_class.points_coordinates.T[0:2]
        d = np.square(d)
        d = np.sum(d.T, axis=1)
        d = np.sqrt(d)
        d = np.ones_like(d)*0.0015 - d

        measurement_volume = cylinder_intersection(d, 0.0015, eulerian_class.radius)

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

        fraction = np.divide(eulerian_class.particle_volume, measurement_volume, out=np.zeros_like(eulerian_class.particle_volume), where=eulerian_class.particle_volume!=0)

        print(eulerian_class.particle_volume)
        print(measurement_volume)
        print(fraction)
        pfractions.append(fraction)

    return pfractions

# Intersection between sphere and cylinder
def cylinder_intersection(d, R, r):
    inRange = (d < r)
    R = np.ones(d.shape)*R
    r = np.ones(d.shape)*r
    volume = np.pi*( 4/3*np.power(r,3*np.ones_like(r)) - 1/3*np.square(r - d)*(2*r + d))
    volume = (volume * inRange) + (np.logical_not(inRange) * (4/3 * np.pi * np.power(r,3*np.ones_like(r))) )

    return volume
