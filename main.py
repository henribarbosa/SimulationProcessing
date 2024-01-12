from src.read_files import time_step_data, simulation_data
from src.bed_points_array import points_array

def main():
    print("Welcome to the processing tool")
    Data = simulation_data("/media/dados0/Mestrado/Leito_Ar/Polydisperse_difelice/Mono_Velocidade_1.77_angle_0/DEM/post/",
                           max_number_files=10)

    Data.build_time_series("types")
    Data.print_data()
    
    Points = points_array(0.0015, 0.1)
    Points.plot_grid()

main()
