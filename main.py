from src.read_files import time_step_data, simulation_data

def main():
    print("Welcome to the processing tool")
    Data = simulation_data("/media/dados0/Mestrado/Leito_Ar/Mono_Velocidade_1.77_angle_0/DEM/post")

    Data.build_time_series_per_particle("positions", 0)
    print(Data.time_series)

main()
