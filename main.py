from src.read_files import time_step_data, simulation_data
from src.bed_points_array import points_array
from src.eulerian_averages import eulerian_average
from src.toolkit import granular_temperature, packing_fraction
from src.graphics import last_quiver_view, last_scalar_view, view_particles, view_average_areas, save_frames_quiver, save_frames_particles
from src.surface import surface

def main():
    print("Welcome to the processing tool")
    Data = simulation_data("/media/dados0/Mestrado/Leito_Ar/Polydisperse_difelice/Mono_Velocidade_1.77_angle_0/DEM/post/",
                           max_number_files=10, skip_step=1)
    # Data = simulation_data("../files/", max_number_files=10)

    # Data.build_time_series("radius")
    # Data.print_data()
    
    # Points = points_array(0.0015, 0.1, dr=0.0005, dtheta=0.5, dz=3*0.0005)
    # Points.plot_grid()

    # AVG = eulerian_average(Data, points=Points)
    # AVG.make_vector_average("velocities")
    # AVG.make_scalar_average("radius")
    # AVG.print_fields()
    # AVG.save_vector_file()

    # AVG.apply_scalar_function(granular_temperature)
    # AVG.apply_scalar_function(packing_fraction)
    # AVG.print_fields()

    # AVG.make_vector_average("velocities")
    # last_quiver_view(Points, AVG.get_vector_data())
    # last_scalar_view(Points, AVG.get_scalar_data())
    # view_average_areas(AVG)
    # view_particles(Data, index=0)
    # save_frames_quiver(Points, AVG.get_vector_data())
    # save_frames_particles(Data)

    superficie = surface(Data)
    superficie.check_surface()
main()
