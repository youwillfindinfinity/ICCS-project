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
endothelial_counts = [
    10, 10, 10, 10, 10,
    100, 100, 100, 100, 100,
    500, 500, 500, 500, 500,
    1000, 1000, 1000, 1000, 1000,
    2000, 2000, 2000, 2000, 2000,
    3000, 3000, 3000, 3000, 3000,
    4000, 4000, 4000, 4000, 4000,
    5000, 5000, 5000, 5000, 5000
]
# endothelial_counts = [
#     10, 10,
#     100, 100,
#     500, 500, 
#     1000, 1000,
#     2000, 2000, 
#     3000, 3000, 
#     4000, 4000,
#     5000, 5000,
# ]

# Loop through each index and read the data
for index in range(len(endothelial_counts)):
    # Construct the path to the simulation_time.txt file
    file_path = os.path.join('ICCS_experiments/snellius_Benchmark_full', f'scan_iteration_{index}', 'combi_clean_benchmarked', 'datafiles', 'simulation_time.txt')
    
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
                'Endothelial Count': endothelial_counts[index],
                'PP_h': pp_h,
                'RP_h': rp_h,
                'IP_h': ip_h - pp_h - rp_h
            })
    else:
        print(f"File not found: {file_path}")

# Convert the list of data into a DataFrame
all_data_df = pd.DataFrame(all_data)

# Save the DataFrame to a CSV file
output_csv_path = os.path.join(results_folder, 'endothelial_simulation_data_phases_endocounts_snellius_Benchmark_full.csv')
all_data_df.to_csv(output_csv_path, index=False)

print(f"Data successfully saved to {output_csv_path}")
