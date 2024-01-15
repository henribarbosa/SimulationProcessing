import numpy as np
from glob import glob

property_list = ["types", "positions", "velocities", "forces", "dragforces",
                 "radius", "densities"]

class time_step_data:
    
    def __init__(self, file_path):
        file = open(file_path, "r")
        
        # time step 
        file.readline()
        self.timestep = int(file.readline())

        # number of atoms
        file.readline()
        self.numAtoms = int(file.readline())

        # box bounds
        for i in range(4):
            file.readline()

        # items to be read
        self.ids = np.arange(self.numAtoms)
        self.types = []
        self.positions = []
        self.velocities = []
        self.forces = []
        self.dragforces = []
        self.radius = []
        self.densities = []

        # loop over the atoms
        file.readline()
        for i in range(self.numAtoms):
            line = file.readline()
            values = [x for x in line.split(' ')]
            self.types.append(int(values[1]))
            self.positions.append([float(x) for x in values[2:5]])
            self.velocities.append([float(x) for x in values[5:8]])
            self.forces.append([float(x) for x in values[8:11]])
            self.dragforces.append([float(x) for x in values[11:14]])
            self.radius.append(float(values[14]))
            self.densities.append(int(values[15]))

        # convert to numpy array
        self.types = np.array(self.types, dtype='uint')
        self.positions = np.array(self.positions, dtype='float32')
        self.velocities = np.array(self.velocities, dtype='float32')
        self.forces = np.array(self.forces, dtype='float32')
        self.dragforces = np.array(self.dragforces, dtype='float32')
        self.radius = np.array(self.radius, dtype='float32')
        self.densities = np.array(self.densities, dtype='uint')
        
class simulation_data:
    def __init__(self,folder_path, max_number_files=0):
        # glob file list of frames
        self.files = glob(folder_path + "/dump_liggghts_run.*")
        if max_number_files != 0:
            self.files = self.files[:max_number_files]

        # store all data in vectors
        self.types = []
        self.positions = []
        self.velocities = []
        self.forces = []
        self.dragforces = []
        self.radius = []
        self.densities = []

        # initialize variables
        self.time_series_vector = []
        self.time_series = np.array([])

    def assemble_vectors(self):
        if ( len(self.types) > 0 ):
            return
        print("Reading files...")
        for file in self.files:
            step_data = time_step_data(file)
            for property in property_list:
                self.__dict__[property].append(step_data.__dict__[property])

        return self
            
    # used to assemble a time series of a single variable
    def build_time_series(self, variable_choice):
        self.assemble_vectors()
        self.time_series_vector = self.__dict__[variable_choice]

        self.time_series = np.array(self.time_series_vector)

        return self

    # used to assemble a time series for a single particle
    def build_time_series_per_particle(self, variable_choice, particle):
        self.assemble_vectors()
        for data in self.__dict__[variable_choice]:
            self.time_series_vector.append(data[particle])

        self.time_series = np.array(self.time_series_vector)

        return self

    # return the time series
    def get_data(self):
        return self.time_series

    # print the time series
    def print_data(self):
        print(self.time_series)

