import os
import pandas as pd

results_folder = 'Parallel_results'

# Check if the folder exists, and create it if it does not
if not os.path.exists(results_folder):
    os.makedirs(results_folder)
    print(f'Folder created: {results_folder}')

# Initialize a list to store the data
all_data = []

endothelial_processor = [
    '1000:4', '5000:4',
    '1000:8', '5000:8',
    '1000:16', '5000:16',
    '1000:32', '5000:32',
    '5000:128'
]

# Corrected index list (remove invalid index 11)
valid_indices = [0, 1, 2, 3, 4, 5, 6, 7]  # Only valid indices

# Loop through each index and read the data
for index in valid_indices:
    # Construct the path to the simulation_time.txt file (use raw string to avoid escape sequence issues)
    file_path = os.path.join(r'ICCS_experiments/snellius_Parallel', f'scan_iteration_{index}', 'combi_clean_parallel', 'datafiles', 'simulation_time.txt')
    
    # Check if the file exists
    if os.path.exists(file_path):
        # Read the data from the file
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # Skip the header (first line) and extract the data line (second line)
            data_line = lines[1].strip()  
            # Split the data into components (PP_h, RP_h, IP_h)
            pp_h, rp_h, ip_h = map(float, data_line.split(','))
            
            # Extract endothelial count and processor number from the string
            endothelial_count, processor_nr = map(int, endothelial_processor[index].split(':'))
            
            # Append the data along with extracted values
            all_data.append({
                'Endothelial Count': endothelial_count,
                'Processor Number': processor_nr,
                'PP_h': pp_h,
                'RP_h': rp_h,
                'IP_h': ip_h
            })
    else:
        print(f"File not found: {file_path}")

# Convert the list of data into a DataFrame
all_data_df = pd.DataFrame(all_data)

# Save the DataFrame to a CSV file
output_csv_path = os.path.join(results_folder, 'parallel_snellius_endocount_processors.csv')
all_data_df.to_csv(output_csv_path, index=False)

print(f"Data successfully saved to {output_csv_path}")
