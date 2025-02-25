import os
import pandas as pd
from scipy.stats import f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Create the results folder if it doesn't exist
results_folder = 'Benchmark_results'
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

# Loop through each index and read the data
for index in range(40):
    # Construct the path to the simulation_time.txt file
    file_path = os.path.join('ICCS_experiments\snellius_Benchmark_full', f'scan_iteration_{index}', 'combi_clean_benchmarked', 'datafiles', 'simulation_time.txt')
    
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
output_csv_path = os.path.join(results_folder, 'endothelial_simulation_data_phases_endocounts.csv')
all_data_df.to_csv(output_csv_path, index=False)
print(f"Data successfully saved to {output_csv_path}")

# Perform ANOVA (Analysis of Variance) for each phase (PP_h, RP_h, IP_h)
phases = ['PP_h', 'RP_h', 'IP_h']
anova_results = {}

for phase in phases:
    # Group data by endothelial count and extract values for ANOVA
    grouped_data = [group[phase].values for _, group in all_data_df.groupby('Endothelial Count')]
    
    # Perform one-way ANOVA test
    f_statistic, p_value = f_oneway(*grouped_data)
    anova_results[phase] = {'F-statistic': f_statistic, 'p-value': p_value}

# Save ANOVA results to a CSV file
anova_results_df = pd.DataFrame(anova_results).T
anova_results_output_path = os.path.join(results_folder, 'anova_results_phases_endocounts.csv')
anova_results_df.to_csv(anova_results_output_path)
print(f"ANOVA results saved to {anova_results_output_path}")

# Perform pairwise Tukey HSD test for each phase if ANOVA is significant
for phase in phases:
    if anova_results[phase]['p-value'] < 0.05:  # Check if ANOVA is significant
        tukey = pairwise_tukeyhsd(
            endog=all_data_df[phase],                # Dependent variable (e.g., PP_h)
            groups=all_data_df['Endothelial Count'], # Independent variable (grouping by count)
            alpha=0.05                               # Significance level
        )
        tukey_output_path = os.path.join(results_folder, f'tukey_{phase}_results_phases_endocounts.txt')
        with open(tukey_output_path, 'w') as f:
            f.write(str(tukey))
        print(f"Tukey HSD results for {phase} saved to {tukey_output_path}")
