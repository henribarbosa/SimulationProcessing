import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src.read_files import simulation_data
from src.eulerian_averages import eulerian_average
from src.surface import surface

# Functions from @Mateen Ulhaq and @karlo
def set_axes_equal(ax: plt.Axes):
    """Set 3D plot axes to equal scale.

    Make axes of 3D plot have equal scale so that spheres appear as
    spheres and cubes as cubes.  Required since `ax.axis('equal')`
    and `ax.set_aspect('equal')` don't work on 3D.
    """
    limits = np.array([
        ax.get_xlim3d(),
        ax.get_ylim3d(),
        ax.get_zlim3d(),
    ])
    origin = np.mean(limits, axis=1)
    radius = 0.5 * np.max(np.abs(limits[:, 1] - limits[:, 0]))
    _set_axes_radius(ax, origin, radius)

def _set_axes_radius(ax, origin, radius):
    x, y, z = origin
    ax.set_xlim3d([x - radius, x + radius])
    ax.set_ylim3d([y - radius, y + radius])
    ax.set_zlim3d([z - radius, z + radius])

def quiver_plot_eulerian(coordinates, data):
    ax = plt.figure().add_subplot(projection='3d')

    points = coordinates.T
    x,y,z = points[0],points[1],points[2]
    vectors = data.T
    u,v,w = vectors[0],vectors[1],vectors[2]

    ax.quiver(x,y,z,u,v,w, normalize=True, length=0.0015)
    ax.set_box_aspect([1,1,1])
    set_axes_equal(ax)

    plt.show()   

def quiver_plot(ax, coordinates, data, index):
    x,y,z = coordinates.export_grid_to_plot()
    vectors = data[index].T
    u,v,w = vectors[0],vectors[1],vectors[2]

    ax.quiver(x,y,z,u,v,w, normalize=True, length=0.0005)
    ax.set_box_aspect([1,1,1])
    set_axes_equal(ax)

def last_quiver_view(coordinates, data, index=-1):
    ax = plt.figure().add_subplot(projection='3d')

    quiver_plot(ax, coordinates, data, index)

    plt.show()

def scalar_plot(ax, coordinates, data, index):
    x,y,z = coordinates.export_grid_to_plot()
    color = data[index]

    ax.scatter(x,y,z,c=color, alpha=0.5)
    ax.set_box_aspect([1,1,1])
    set_axes_equal(ax)

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
    ax.set_box_aspect([1,1,1])
    set_axes_equal(ax)

    
def view_particles(simulation_data, index=-1):
    ax = plt.figure().add_subplot(projection='3d')

    particles_plot(ax, simulation_data, index)

    plt.show()

def surface_plot(ax, surface_data: surface, index):
    coordinates = surface_data.positions[index].T
    type = surface_data.particle_classification[index]

    x,y,z = coordinates[0],coordinates[1],coordinates[2]

    ax.scatter(x,y,z,c=type, alpha=0.7)
    ax.set_box_aspect([1,1,1])
    set_axes_equal(ax)

def view_surface(surface_data: surface, index=-1):
    ax = plt.figure().add_subplot(projection='3d')

    surface_plot(ax, surface_data, index)

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

    ax.set_box_aspect([1,1,1])
    set_axes_equal(ax)

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



