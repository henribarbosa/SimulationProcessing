from src.read_files import time_step_data, simulation_data

def main():
    print("Welcome to the processing tool")
    Data = simulation_data("/home/henrique/Documents/Unicamp/Mestrado/files",
                           max_number_files=10)

    Data.build_time_series_per_particle("positions", 5)
    Data.print_data()

    Data.build_time_series("types")
    Data.print_data()

main()
