import os
import pandas as pd

results_folder = 'Benchmark_results'

# Check if the folder exists, and create it if it does not
if not os.path.exists(results_folder):
    os.makedirs(results_folder)
    print(f'Folder created: {results_folder}')
# Initialize a list to store the data
all_data = []

# Define the endothelial counts corresponding to each index
processor_nr = [
    1, 1, 1, 1, 1,
    2, 2, 2, 2, 2,
    4, 4, 4, 4, 4,
    8, 8, 8, 8, 8,
    16
]
# processor_nr = [1, 2, 4, 8, 16, 32, 64, 128]
# Loop through each index and read the data
for index in range(len(processor_nr)):
    # Construct the path to the simulation_time.txt file
    # file_path = os.path.join('ICCS_experiments\Processor_nr_endothelial_experiment', f'scan_iteration_{index}', 'combi_clean_benchmarked_processors', 'datafiles', 'simulation_time.txt')
    file_path = os.path.join('ICCS_experiments/snellius_Benchmark_process_nr_full', f'scan_iteration_{index}', 'combi_clean_benchmarked_processors', 'datafiles', 'simulation_time.txt')
    # Check if the file exists
    if os.path.exists(file_path):
        # Read the data from the file
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # Skip the header (first line) and extract the data line (second line)
            data_line = lines[1].strip()  
            # Split the data into components (PP_h, RP_h, IP_h)
            pp_h, rp_h, ip_h = map(float, data_line.split(','))
            # Append the data along with the endothelial count
            all_data.append({
                'Processor nr': processor_nr[index],
                'Total sim time' : ip_h
            })
    else:
        print(f"File not found: {file_path}")

# Convert the list of data into a DataFrame
all_data_df = pd.DataFrame(all_data)

# Save the DataFrame to a CSV file
output_csv_path = os.path.join(results_folder, 'processor_nr_exp_full.csv')
all_data_df.to_csv(output_csv_path, index=False)

print(f"Data successfully saved to {output_csv_path}")
