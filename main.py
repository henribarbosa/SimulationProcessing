from src.read_files import time_step_data, simulation_data
from src.bed_points_array import points_array
from src.eulerian_averages import eulerian_average

def main():
    print("Welcome to the processing tool")
    # Data = simulation_data("/media/dados0/Mestrado/Leito_Ar/Polydisperse_difelice/Mono_Velocidade_1.77_angle_0/DEM/post/",
                           # max_number_files=10)
    Data = simulation_data("../files/", max_number_files=10)

    Data.build_time_series("types")
    # Data.print_data()
    
    Points = points_array(0.0015, 0.1, dr=0.0005, dtheta=0.5, dz=0.005)
    # Points.plot_grid()

    AVG = eulerian_average(Data, points=Points)    
    AVG.make_vector_average("velocities")
    print(AVG.average_vector)
    AVG.save_vector_file()

main()
