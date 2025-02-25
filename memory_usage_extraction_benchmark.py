import os
import pandas as pd

results_folder = 'Benchmark_results'
endothelial_counts = [
    10, 10, 10, 10, 10,
    100, 100,100, 100, 100,
    500, 500, 500, 500, 500,
    1000, 1000,1000, 1000, 1000,
    2000, 2000, 2000, 2000, 2000,
    3000, 3000, 3000, 3000, 3000,
    4000, 4000, 4000, 4000, 4000,
    5000, 5000, 5000, 5000, 5000
]
# Example list of indices (replace endothelial_counts with the actual range or list)
endothelial_counts = range(len(endothelial_counts))  # Replace with the actual number of iterations

# Initialize an empty list to store data from all files
all_data = []

# Loop through each index and process the corresponding file
for index in endothelial_counts:
    # Construct the file path
    file_path = os.path.join(
        'ICCS_experiments', 
        'snellius_Benchmark_full', 
        f'scan_iteration_{index}', 
        'combi_clean_benchmarked', 
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
                        mcs_part, memory_part = line.split(":", 1)  # Split only on the first ":"
                        
                        # Extract MCS value
                        mcs = int(mcs_part.split()[1])  # Extract number after "MCS"
                        
                        # Extract memory value in kB (remove "kB" at the end)
                        memory_kb = int(memory_part.strip().split()[1])  # Extract memory value

                        # Convert memory from kB to MB
                        memory_mb = memory_kb / 1024

                        # Append the data as a dictionary
                        all_data.append({
                            'Index': index,
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
output_csv_path = os.path.join(results_folder, "benchmark_combined_memory_usage.csv")
df.to_csv(output_csv_path, index=False)

print(f"Data has been saved to {output_csv_path}")
