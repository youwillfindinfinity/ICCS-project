import pandas as pd
from scipy.stats import f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import os

# File paths
input_csv_path = r'Benchmark_results\processor_nr_exp.csv'
results_folder = r'Benchmark_results'

# Read the input CSV file
data = pd.read_csv(input_csv_path)

# Perform ANOVA for Total sim time grouped by Processor nr
grouped_data = [group['Total sim time'].values for _, group in data.groupby('Processor nr')]
f_statistic, p_value = f_oneway(*grouped_data)

# Save ANOVA results to a CSV file
anova_results = {'F-statistic': f_statistic, 'p-value': p_value}
anova_results_df = pd.DataFrame([anova_results])
anova_results_output_path = os.path.join(results_folder, 'anova_results_sim_time.csv')
anova_results_df.to_csv(anova_results_output_path, index=False)
print(f"ANOVA results saved to {anova_results_output_path}")

# Perform Tukey HSD test if ANOVA is significant
if p_value < 0.05:  # Check if ANOVA is significant
    tukey = pairwise_tukeyhsd(
        endog=data['Total sim time'],         # Dependent variable (Total sim time)
        groups=data['Processor nr'],          # Independent variable (Processor nr)
        alpha=0.05                            # Significance level
    )
    tukey_output_path = os.path.join(results_folder, 'tukey_sim_time_results.txt')
    with open(tukey_output_path, 'w') as f:
        f.write(str(tukey))
    print(f"Tukey HSD results saved to {tukey_output_path}")
