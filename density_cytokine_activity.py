import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from the mean_concentration.txt file
data_file = 'ICCS_experiments/pc_endothelial_benchmarkWholeData/datafiles/mean_concentration.txt'  # Update this path if necessary

# Read the data
data = pd.read_csv(data_file)

# Calculate the rate of change (activity) for each cytokine
cytokines = ['il8mean', 'il1mean', 'il6mean', 'il10mean', 'tnfmean', 'tgfmean']
cytokine_labels = ['il8', 'il1', 'il6', 'il10', 'tnf', 'tgf']  # Custom labels for legend
activity_data = data[cytokines].diff()  # Calculate the difference between consecutive rows

# Add meanconcen (MCS) back to the activity data for reference
activity_data['meanconcen'] = data['meanconcen']

# Remove rows with NaN values (first row after diff will be NaN)
# activity_data = activity_data.dropna()

# Clip negative values (set them to 0) to avoid passing negative weights
activity_data[cytokines] = activity_data[cytokines].clip(lower=0)

# Normalize cytokine activities so that they are between 0 and 1
total_activity_per_step = activity_data[cytokines].sum(axis=1)  # Sum of all cytokine activities per step
for cytokine in cytokines:
    activity_data[cytokine] /= total_activity_per_step  # Normalize each cytokine by the total activity

# Generate a hot-to-cold color palette
colors = sns.color_palette("seismic_r", len(cytokines))  # Hot-to-cold colors

# Plot density plots for each cytokine's normalized activity over MCS
plt.figure(figsize=(20, 4))  # Adjust figsize for better visualization

for cytokine, label, color in zip(cytokines, cytokine_labels, colors):
    plt.plot(
        activity_data['meanconcen'],
        activity_data[cytokine],
        label=label,
        color=color,
        linewidth=2,
    )
    plt.fill_between(
        activity_data['meanconcen'],
        activity_data[cytokine],
        color=color,
        alpha=0.3,
    )

# Add labels and title
plt.xlabel('MCS (MeanConcen)', fontsize=14)
plt.ylabel('Proportion (Normalized)', fontsize=14)
plt.title('Normalized Cytokine Activity Over MCS (Hot-to-Cold Colors)', fontsize=16)

# Add legend outside the plot with custom labels
plt.legend(title="Cytokines", bbox_to_anchor=(1.05, 1), loc='upper left')

# Ensure the plot starts at meanconcen = 0
plt.xlim(0, data['meanconcen'].max())
plt.ylim(0, 1)  # Set y-axis range between 0 and 1

# Add gridlines for better readability
plt.grid(True, linestyle="--", linewidth=0.5)

# Remove upper and right spines
sns.despine()

# Save the plot as a PNG file
plt.tight_layout()
# plt.savefig("Benchmark_results/cytokine_activity_plot.png", dpi=400, transparent=True)
plt.show()
