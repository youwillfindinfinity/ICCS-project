import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# File paths
# data_file = r'Benchmark_results\processor_nr_exp.csv'
data_file = r'Benchmark_results\processor_nr_exp_full.csv'
results_folder = r'Benchmark_results'

# Load the data from the CSV file
data = pd.read_csv(data_file)

# Create the results folder if it doesn't exist
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

# Set Seaborn style for better aesthetics
sns.set_theme(style="whitegrid")

# Create a violin plot for Total sim time grouped by Processor nr
plt.figure(figsize=(10, 6))

# Create a color palette based on Total sim time (for aesthetic purposes)
cmap = sns.color_palette("coolwarm", as_cmap=True)
norm = plt.Normalize(vmin=data['Total sim time'].min(), vmax=data['Total sim time'].max())
colors = cmap(norm(data['Total sim time']).data).tolist()

# Create the violin plot
ax = sns.violinplot(
    x='Processor nr', 
    y='Total sim time', 
    data=data, 
    inner=None,  # Disable internal lines for a cleaner look
    palette="muted"  # Use a predefined Seaborn palette for simplicity
)

# Overlay mean lines for each processor group
means = data.groupby('Processor nr')['Total sim time'].mean()
for i, mean in enumerate(means):
    ax.plot([i - 0.2, i + 0.2], [mean, mean], color='black', linewidth=4, label='Mean' if i == 0 else "")

# Customize the plot with titles and labels
plt.title('Violin Plot of Total Simulation Time by Processor Number', fontsize=16)
plt.xlabel('Processor Number', fontsize=14)
plt.ylabel('Total Simulation Time (hours)', fontsize=14)

# Save the plot as a PNG file in the results folder
output_file = os.path.join(results_folder, 'violin_plot_total_sim_time_per_processor_snellius_full.png')
plt.savefig(output_file, dpi=300)  # High-resolution output

print(f"Saved {output_file}")

# Close the plot to avoid overlapping figures in future plots
plt.close()
