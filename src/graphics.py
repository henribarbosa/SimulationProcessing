import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src.read_files import simulation_data
from src.eulerian_averages import eulerian_average

def quiver_plot(ax, coordinates, data, index):
    x,y,z = coordinates.export_grid_to_plot()
    vectors = data[index].T
    u,v,w = vectors[0],vectors[1],vectors[2]

    ax.quiver(x,y,z,u,v,w, normalize=True, length=0.0005)

def last_quiver_view(coordinates, data, index=-1):
    ax = plt.figure().add_subplot(projection='3d')

    quiver_plot(ax, coordinates, data, index)

    plt.show()

def scalar_plot(ax, coordinates, data, index):
    x,y,z = coordinates.export_grid_to_plot()
    color = data[index]

    ax.scatter(x,y,z,c=color, alpha=0.5)

def last_scalar_view(coordinates, data, index=-1):
    ax = plt.figure().add_subplot(projection='3d')

    scalar_plot(ax, coordinates, data, index)

    plt.show()

def particles_plot(ax, simulation_data, index):
    coordinates = simulation_data.build_time_series("positions").get_data()[index].T
    velocities = simulation_data.build_time_series("velocities").get_data()[index].T

    x,y,z = coordinates[0],coordinates[1],coordinates[2]
    u,v,w = velocities[0],velocities[1],velocities[2]

    ax.quiver(x,y,z,u,v,w, normalize=True, length=0.0003)
    ax.scatter(x,y,z,c=np.sqrt(u**2+v**2+w**2), alpha=0.5)

    
def view_particles(simulation_data, index=-1):
    ax = plt.figure().add_subplot(projection='3d')

    particles_plot(ax, simulation_data, index)

    plt.show()

def view_average_areas(eulerian_data):
    ax = plt.figure().add_subplot(projection='3d')

    r = eulerian_data.radius
    u = np.linspace(0, 2*np.pi, 26)
    v = np.linspace(0, np.pi, 26)
    x_sph = r * np.outer(np.cos(u), np.sin(v))
    y_sph = r * np.outer(np.sin(u), np.sin(v))
    z_sph = r * np.outer(np.ones(np.size(u)), np.cos(v))

    x,y,z = eulerian_data.points_coordinates.T[0],eulerian_data.points_coordinates.T[1],eulerian_data.points_coordinates.T[2]

    for i in range(0,eulerian_data.number_points,100):
        ax.plot_surface(x[i] + x_sph, y[i] + y_sph, z[i] + z_sph, color='b')

    plt.show()

def save_frames_quiver(coordinates, data):
    print("Saving animation frames...")
    ax = plt.figure().add_subplot(projection='3d')

    for i in range(len(data)):
        quiver_plot(ax, coordinates, data, i)
        plt.savefig("Frames/frame_"+str(i).zfill(5)+".png", dpi=500, bbox_inches = "tight")
        plt.cla()

def save_frames_particles(simulation_data):
    print("Saving particles frames")
    ax = plt.figure().add_subplot(projection='3d')

    for i in range(len(simulation_data.files)):
        particles_plot(ax, simulation_data, i)
        plt.savefig("Frames/frame_"+str(i).zfill(5)+".png", dpi=500, bbox_inches = "tight")
        plt.cla()



