import numpy as np
from src.bed_points_array import points_array
from src.read_files import time_step_data, simulation_data
from src.utils import clear_file

# Volume of sphere intersection
def sphere_intersection(d, R, r):
    inRange = np.logical_or(d > (R-r), d < (R+r))
    R = np.ones(d.shape)*R
    r = np.ones(d.shape)*r
    volume = np.pi/(12*d)*(np.square(d) + 2*d*r - 3*np.square(r) + 2*d*R + 6*r*R - 3*np.square(R))*np.square((R + r - d))
    return volume * inRange

# Average the desired measument in the points of the bed
class eulerian_average:
    def __init__(self, lagrangian_data, points=points_array(0.0015,0.1), radius=0.003):
        self.times = len(lagrangian_data.files)
        self.number_points = points.n_total
        self.radius = radius # Influence radius 
        self.avg_quantity = ""

        self.points_coordinates = np.vstack((np.array(points.points_x),
                                             np.array(points.points_y),
                                             np.array(points.points_z))).T

        self.lagrangian_data = lagrangian_data
        self.positions = lagrangian_data.build_time_series("positions").get_data()
        self.particle_volume = np.zeros([self.times, points.n_total])
        self.average_scalar = np.zeros([self.times, points.n_total])
        self.average_vector = np.zeros([self.times, points.n_total, 3])


    def make_scalar_average(self, property):
        print("Making Eulerian average...")

        self.avg_quantity = property
        data = self.lagrangian_data.build_time_series(property).get_data()

        for timeDataIndex in range(len(data)):
            self.particle_volume = np.zeros([self.times, self.number_points])
            for particleIndex in range(len(data[0])):
                particle_position = np.vstack(
                 (np.ones(self.number_points)*self.positions[timeDataIndex][particleIndex][0],
                  np.ones(self.number_points)*self.positions[timeDataIndex][particleIndex][1],
                  np.ones(self.number_points)*self.positions[timeDataIndex][particleIndex][2])).T
                delta = self.points_coordinates - particle_position
                delta = np.square(delta)
                delta = np.sum(delta, axis=1)
                delta = np.sqrt(delta) # distance between particle and point

                volume = sphere_intersection(delta, self.radius, self.lagrangian_data.radius[timeDataIndex][particleIndex])
                self.particle_volume = self.particle_volume + volume
                self.average_scalar = self.average_scalar + volume * data[timeDataIndex][particleIndex]

        self.average_scalar = np.divide(self.average_scalar, self.particle_volume)

        return self

    def make_vector_average(self, property):
        print("Making Eulerian average...")

        self.avg_quantity = property
        data = self.lagrangian_data.build_time_series(property).get_data()

        for timeDataIndex in range(len(data)):
            self.particle_volume = np.zeros([self.times, self.number_points])
            for particleIndex in range(len(data[0])):
                particle_position = np.vstack(
                 (np.ones(self.number_points)*self.positions[timeDataIndex][particleIndex][0],
                  np.ones(self.number_points)*self.positions[timeDataIndex][particleIndex][1],
                  np.ones(self.number_points)*self.positions[timeDataIndex][particleIndex][2])).T
                delta = self.points_coordinates - particle_position
                delta = np.square(delta)
                delta = np.sum(delta, axis=1)
                delta = np.sqrt(delta) # distance between particle and point

                volume = sphere_intersection(delta, self.radius, self.lagrangian_data.radius[timeDataIndex][particleIndex])
                self.particle_volume = self.particle_volume + volume
                self.average_vector = self.average_vector + np.outer(volume, data[timeDataIndex][particleIndex])

        self.average_vector = np.divide(self.average_vector, np.array([self.particle_volume, self.particle_volume, self.particle_volume]).transpose((1,2,0)))

        return self

    def save_scalar_file(self):
        print("Saving eulerian file...")
        clear_file("Files/"+self.avg_quantity+".txt")

        f = open("Files/"+self.avg_quantity+".txt", "a")
        f.write("{:d}\n".format(self.times))
        f.write("{:d}\n".format(self.number_points))
        for time in self.average_scalar:
            for point in time:
                f.write("{:.5f}\n".format(point))
        f.close()

        return self

    def save_vector_file(self):
        print("Saving eulerian file...")
        clear_file("Files/"+self.avg_quantity+".txt")

        f = open("Files/"+self.avg_quantity+".txt", "a")
        f.write("{:d}\n".format(self.times))
        f.write("{:d}\n".format(self.number_points))
        for time in self.average_vector:
            for point in time:
                f.write("{:.5f}   {:.5f}   {:.5f}\n".format(point[0], point[1], point[2]))
        f.close()

        return self

    def get_scalar_data(self):
        return self.average_scalar

    def get_vector_data(self):
        return self.average_vector


