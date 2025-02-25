import os
import pandas as pd

# Define the results folder for saving the output
results_folder = 'Parallel_results'

# Ensure the results folder exists
if not os.path.exists(results_folder):
    os.makedirs(results_folder)
    print(f"Folder created: {results_folder}")

# Define the indices for endothelial counts (replace with actual range or list)
endothelial_counts = [
    '1000', '5000',
    '1000', '5000',
    '1000', '5000',
    '1000', '5000',
    '5000'
]
indices = range(len(endothelial_counts))  # Replace with actual number of iterations if different

# Initialize an empty list to store data from all files
all_data = []

# Loop through each index and process the corresponding file
for index in indices:
    if index == 8:
        index = 11
    else:
        # Construct the file path for memory_log.txt
        file_path = os.path.join(
            'ICCS_experiments', 
            'snellius_Parallel', 
            f'scan_iteration_{index}', 
            'combi_clean_parallel', 
            'datafiles', 
            'Memory usage', 
            'memory_log.txt'
        )
    
    # Check if the file exists before processing
    if os.path.exists(file_path):
        # Open and read the file
        with open(file_path, 'r') as file:
            for line in file:
                # Ensure the line contains "MCS" and "VmRSS"
                if "MCS" in line and "VmRSS" in line:
                    try:
                        # Split the line by ":" and extract MCS and memory values
                        parts = line.split(":")
                        
                        # Extract MCS value (assumes "MCS <value>")
                        mcs_part = parts[0].strip()
                        mcs = int(mcs_part.split()[1])  # Extract number after "MCS"
                        
                        # Extract memory value in kB (assumes "VmRSS: <value> kB")
                        memory_part = parts[1].strip()
                        memory_kb = int(memory_part.split()[0])  # Extract memory value

                        # Convert memory from kB to MB
                        memory_mb = memory_kb / 1024

                        # Append the data as a dictionary
                        all_data.append({
                            'Index': index,
                            'Endothelial Count': endothelial_counts[index],
                            'MCS': mcs,
                            'Memory (MB)': memory_mb
                        })
                    except (IndexError, ValueError) as e:
                        print(f"Error parsing line: {line.strip()} in file {file_path}. Error: {e}")
    else:
        print(f"File not found: {file_path}")

# Convert the collected data into a DataFrame
df = pd.DataFrame(all_data)

# Save the DataFrame to a CSV file
output_csv_path = os.path.join(results_folder, "combined_memory_usage_parallel.csv")
df.to_csv(output_csv_path, index=False)

print(f"Data has been saved to {output_csv_path}")
