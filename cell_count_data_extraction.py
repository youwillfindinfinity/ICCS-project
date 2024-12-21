import os
import pandas as pd

# Define the results folder
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

# Define the MCS values for each phase
mcs_values = [240000, 720000, int(1e6)] # Proliferative Phase (PP_h), Remodeling Phase (RP_h), Inflammatory Phase (IP_h)

# Loop through each index and read the data
for index in range(40):
    # Construct the path to the cellcount.txt file
    file_path = os.path.join('ICCS_experiments/endothelialParameterScanBenchmark', f'scan_iteration_{index}', 'combi_clean_benchmarked', 'datafiles', 'cellcount.txt')
    
    # Check if the file exists
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # Process each line after the header (skip header)
            for line in lines[1:]:
                parts = line.strip().split(',')
                if len(parts) > 1 and parts[0].isdigit(): # Ensure valid data and numeric mcsteps
                    mcs = int(parts[0])   # Extract MCS value from the first column
                    total_cells = sum(map(float, parts[1:]))   # Sum all cell counts
                    
                    # Determine the phase based on MCS value
                    if mcs == mcs_values[0]:
                        phase = 'PP_h'   # Proliferative Phase
                    elif mcs == mcs_values[1]:
                        phase = 'RP_h'   # Remodeling Phase
                    elif mcs == mcs_values[2]:
                        phase = 'IP_h'   # Inflammatory Phase
                    else:
                        continue
                    
                    # Append the data along with endothelial count and phase information
                    all_data.append({
                        'Endothelial Count': endothelial_counts[index],
                        'Phase': phase,
                        'MCS': mcs,
                        'Total Cells': total_cells
                    })
                else:
                    print(f"Skipping invalid line in {file_path}: {line.strip()}")
    else:
        print(f"File not found: {file_path}")

# Convert the list of data into a DataFrame
all_data_df = pd.DataFrame(all_data)

# Save the DataFrame to a CSV file
output_csv_path = os.path.join(results_folder, 'endothelial_cell_counts_phases.csv')
all_data_df.to_csv(output_csv_path, index=False)

print(f"Data successfully saved to {output_csv_path}")
