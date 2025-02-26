import os
import pandas as pd
from scipy.stats import f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Define the results folder
results_folder = 'Benchmark_results'
if not os.path.exists(results_folder):
    os.makedirs(results_folder)
    print(f'Folder created: {results_folder}')

# Load the extracted data from the CSV file
data_file = os.path.join(results_folder, 'snellius_benchmark_endothelial_cell_counts_phases_full.csv')

# Check if the file exists
if not os.path.exists(data_file):
    print(f"File not found: {data_file}. Please ensure the data extraction step was completed correctly.")
    exit()

# Load the data into a DataFrame
all_data_df = pd.read_csv(data_file)

# Filter data for the inflammatory phase (IP_h) since we are testing total simulation time
ip_h_data = all_data_df[all_data_df['Phase'] == 'IP_h']

# Check for missing or insufficient data
if ip_h_data.empty:
    print("No data available for the inflammatory phase (IP_h). Please check your dataset.")
    exit()

# Ensure there are enough data points in each group for ANOVA
grouped_by_total_cells = [
    group['MCS'].values for _, group in ip_h_data.groupby('Total Cells') if len(group) > 1
]

# Check if there are enough groups with sufficient data for ANOVA
if len(grouped_by_total_cells) < 2:
    print("Not enough groups with sufficient data for ANOVA. Ensure each group has at least two data points.")
    exit()

# Perform ANOVA (Analysis of Variance)
f_statistic_cells, p_value_cells = f_oneway(*grouped_by_total_cells)

# Save ANOVA results to a CSV file
anova_results = {
    'Total Cells': {'F-statistic': f_statistic_cells, 'p-value': p_value_cells}
}
anova_results_df = pd.DataFrame(anova_results).T
anova_results_output_path = os.path.join(results_folder, 'anova_results_total_cells_simulation_time.csv')
anova_results_df.to_csv(anova_results_output_path)
print(f"ANOVA results saved to {anova_results_output_path}")

# Perform pairwise Tukey HSD test if ANOVA is significant
if p_value_cells < 0.05:  # Check if ANOVA for Total Cells is significant
    tukey_cells = pairwise_tukeyhsd(
        endog=ip_h_data['MCS'],                  # Dependent variable (Simulation Time via MCS)
        groups=ip_h_data['Total Cells'],         # Independent variable (Total Cells)
        alpha=0.05                               # Significance level
    )
    tukey_cells_output_path = os.path.join(results_folder, 'tukey_total_cells_simulation_time.txt')
    with open(tukey_cells_output_path, 'w') as f:
        f.write(str(tukey_cells))
    print(f"Tukey HSD results for Total Cells saved to {tukey_cells_output_path}")
else:
    print("ANOVA did not find significant differences. Tukey HSD test was not performed.")
