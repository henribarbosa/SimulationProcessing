import numpy as np
from src.bed_points_array import points_array
from src.read_files import time_step_data, simulation_data
from src.utils import clear_file

# Volume of sphere intersection
def sphere_intersection(d, R, r):
    inRange = np.logical_and(d > (R-r), d < (R+r))
    R = np.ones(d.shape)*R
    r = np.ones(d.shape)*r
    volume = np.pi/12 * np.divide((np.square(d) + 2*d*r - 3*np.square(r) + 2*d*R + 6*r*R - 3*np.square(R))*np.square((R + r - d)), d, out=np.zeros_like(d), where=d!=0)
    return volume * inRange

# Average the desired measument in the points of the bed
class eulerian_average:
    def __init__(self, lagrangian_data, points=points_array(0.0015,0.1), r_in=0.0005):
        self.times = len(lagrangian_data.files)
        self.number_points = points.n_total
        self.radius = r_in # Influence radius 
        self.avg_quantity = ""

        self.points_coordinates = np.vstack((np.array(points.points_x),
                                             np.array(points.points_y),
                                             np.array(points.points_z))).T

        self.lagrangian_data = lagrangian_data
        self.positions = lagrangian_data.build_time_series("positions").get_data()
        self.particle_volume = np.zeros([points.n_total])
        self.average_scalar = np.zeros([self.times, points.n_total])
        self.average_vector = np.zeros([self.times, points.n_total, 3])

    def change_radius(self, new_radius):
        self.radius = new_radius
        return self

    def make_scalar_average(self, property):
        print("Making Eulerian average...")

        self.avg_quantity = property
        data = self.lagrangian_data.build_time_series(property).get_data()

        for timeDataIndex in range(len(data)):
            self.particle_volume = np.zeros([self.number_points])
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
                 self.average_scalar[timeDataIndex] = self.average_scalar[timeDataIndex] + volume * data[timeDataIndex][particleIndex]

            self.average_scalar[timeDataIndex] = np.divide(self.average_scalar[timeDataIndex], self.particle_volume, out=np.zeros_like(self.average_scalar[timeDataIndex]), where=self.particle_volume!=0)

        return self

    def make_vector_average(self, property):
        print("Making Eulerian average...")

        self.avg_quantity = property
        data = self.lagrangian_data.build_time_series(property).get_data()

        for timeDataIndex in range(len(data)):
            self.particle_volume = np.zeros([self.number_points])
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
                self.average_vector[timeDataIndex] = self.average_vector[timeDataIndex] + np.outer(data[timeDataIndex][particleIndex], volume).T

            self.average_vector[timeDataIndex] = np.divide(self.average_vector[timeDataIndex], np.array([self.particle_volume, self.particle_volume, self.particle_volume]).T, out=np.zeros_like(self.average_vector[timeDataIndex]), where=np.array([self.particle_volume, self.particle_volume, self.particle_volume]).T!=0)

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

    def apply_scalar_function(self, function):
        self.average_scalar = function(self)
        return self

    def apply_vector_function(self, function):
        self.average_vector = function(self)
        return self

    def print_scalar_field(self):
        print(self.average_scalar)
        return self

    def print_vector_field(self):
        print(self.average_vector)
        return self

    def print_fields(self):
        self.print_scalar_field()
        self.print_vector_field()
        return self

