import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.ndimage import gaussian_filter1d

# Load the data from the mean_concentration.txt file
data_file = 'ICCS_experiments/pc_endothelial_benchmarkWholeData/datafiles/mean_concentration.txt'  # Update this path if necessary

# Read the data
data = pd.read_csv(data_file)

# Calculate the rate of change (activity) for each cytokine
cytokines = ['il8mean', 'il1mean', 'il6mean', 'il10mean', 'tnfmean', 'tgfmean']
cytokine_labels = ['il8', 'il1', 'il6', 'il10', 'tnf', 'tgf']  # Custom labels for legend
activity_data = data[cytokines].diff()  # Calculate the difference between consecutive rows


# Smooth the cytokine activity using a Gaussian filter
cytokines = ['il8mean', 'il1mean', 'il6mean', 'il10mean', 'tnfmean', 'tgfmean']
smoothed_data = data[cytokines].apply(lambda x: gaussian_filter1d(x, sigma=2))

# Normalize cytokine activities so that they are between 0 and 1
total_activity_per_step = smoothed_data.sum(axis=1)
normalized_data = smoothed_data.div(total_activity_per_step, axis=0)

# Add meanconcen (MCS) back for reference
normalized_data['meanconcen'] = data['meanconcen']

# Generate a hot-to-cold color palette
colors = sns.color_palette("seismic_r", len(cytokines))

# Plot density-like curves for each cytokine's normalized activity over MCS
plt.figure(figsize=(20, 4))

for cytokine, color in zip(cytokines, colors):
    plt.plot(
        normalized_data['meanconcen'],
        normalized_data[cytokine],
        label=cytokine.replace('mean', '').upper(),
        color=color,
        linewidth=4,
    )
    plt.fill_between(
        normalized_data['meanconcen'],
        normalized_data[cytokine],
        color=color,
        alpha=0.3,
    )

# Add labels and title
# plt.xlabel('MCS (MeanConcen)', fontsize=14)
# plt.ylabel('Proportion (Normalized)', fontsize=14)
# plt.title('Smoothed and Normalized Cytokine Activity Over MCS', fontsize=16)

# Add legend outside the plot with custom labels
plt.legend(title="Cytokines", bbox_to_anchor=(1.05, 1), loc='upper left')

# Add gridlines for better readability
# plt.grid(True, linestyle="--", linewidth=0.5)
plt.xlim([0,1e6])
plt.ylim([0,1])

# Remove upper and right spines
sns.despine()

plt.tight_layout()
plt.savefig("Benchmark_results/cytokine_activity_plot.png", dpi=400, transparent=True)
plt.show()
