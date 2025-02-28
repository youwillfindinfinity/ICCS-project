import os
import pandas as pd

# Define output folder
results_folder = 'Parallel_results'

# Check if the folder exists, and create it if it does not
if not os.path.exists(results_folder):
    os.makedirs(results_folder)
    print(f'Folder created: {results_folder}')

# Initialize a list to store the data
all_data = []

# Define processor numbers and endothelial counts corresponding to each index
processor_nr = [
    1, 1, 1, 1, 1,
    2, 2, 2, 2, 2,
    4, 4, 
    6, 6,
    8, 8, 8
]
endothelial_counts = [
    1000, 1000, 1000, 1000, 1000,
    1000, 1000, 1000, 1000, 1000,
    1000, 1000, 
    1000, 1000,
    1000, 1000, 1000
]

# Loop through each index and read the data from both processor and endothelial count experiments
for index in range(len(processor_nr)):

    # Construct file paths for processor-based and endothelial-based experiments
    processor_file_path = os.path.join(
        'ICCS_experiments/snellius_Parallel',
        f'scan_iteration_{index}',
        'combi_clean_parallel',
        'datafiles',
        'simulation_time.txt'
    )

    # Read processor-based data if it exists
    if os.path.exists(processor_file_path):
        with open(processor_file_path, 'r') as file:
            lines = file.readlines()
            data_line = lines[1].strip()  
            pp_h_proc, rp_h_proc, ip_h_proc = map(float, data_line.split(','))
            all_data.append({
                'Processor nr': processor_nr[index],
                'Endothelial Count': endothelial_counts[index],
                'PP_h': pp_h_proc,
                'RP_h': rp_h_proc,
                'IP_h': ip_h_proc - pp_h_proc - rp_h_proc,
                'Total sim time': ip_h_proc
            })
    else:
        print(f"Processor-based file not found: {processor_file_path}")

   

# Convert the list of data into a DataFrame
all_data_df = pd.DataFrame(all_data)

# Save the DataFrame to a CSV file
output_csv_path = os.path.join(results_folder, 'eficalc_input_par_comp.csv')
all_data_df.to_csv(output_csv_path, index=False)

print(f"Data successfully saved to {output_csv_path}")
