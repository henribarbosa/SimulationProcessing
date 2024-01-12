import numpy as np
import matplotlib.pyplot as plt

class points_array:
    # array of points for a tube of radius r and height h
    # with dr, dtheta and dz for the grid of points
    def __init__(self, r, h, dr=0.0001, dtheta=0.1, dz=0.001):
        
        # number of points in each direction
        self.n_r = int(r/dr)+1
        self.n_theta = int(2*np.pi/dtheta)+1
        self.n_h = int(h/dz)+1
        self.n_total = self.n_r * self.n_theta * self.n_h

        # build the grid of points 
        self.points_r = np.linspace(0,r,num=self.n_r)
        self.points_theta = np.linspace(0,2*np.pi,num=self.n_theta)
        self.points_h = np.linspace(0,h,num=self.n_h)

        self.points_x = []
        self.points_y = []
        self.points_z = []
        for r in self.points_r:
            for theta in self.points_theta:
                for z in self.points_h:
                    self.points_x.append(r * np.cos(theta))
                    self.points_y.append(r * np.sin(theta))
                    self.points_z.append(z)


    def plot_grid(self):
        print("Numero de pontos total {:3d}".format(self.n_total))
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.scatter(self.points_x, self.points_y, self.points_z)
        plt.show()



