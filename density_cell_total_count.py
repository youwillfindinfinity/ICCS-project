import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from the cellcount.txt file
data_file = 'ICCS_experiments/endothelial_benchmarkWholeData/datafiles/cellcount.txt'  # Update this path if necessary

# Read the data
data = pd.read_csv(data_file)

# Define cell type classifications
cell_types = {
    1: 'Neutral',
    2: 'Inflammatory', 3: 'Inflammatory', 5: 'Inflammatory',
    6: 'Inflammatory', 7: 'Inflammatory', 8: 'Inflammatory',
    4: 'Remodeling', 10: 'Remodeling',
    9: 'Anti-inflammatory'
}

# Initialize columns for each cell type
data['Neutral'] = data.iloc[:, 1:2].sum(axis=1)  # Column for cell type 1
data['Inflammatory'] = data.iloc[:, [2, 3, 5, 6, 7, 8]].sum(axis=1)  # Columns for cell types 2,3,5,6,7,8
data['Remodeling'] = data.iloc[:, [4, 10]].sum(axis=1)  # Columns for cell types 4 and 10
data['Anti-inflammatory'] = data.iloc[:, [9]].sum(axis=1)  # Column for cell type 9

# Plot the density plot for each cell type
plt.figure(figsize=(20, 2))  # Adjust figsize for better visualization

sns.kdeplot(data=data, x='mcsteps', weights='Neutral', fill=True, color='black', alpha=0.6, label='Neutral', linewidth=4)
sns.kdeplot(data=data, x='mcsteps', weights='Inflammatory', fill=True, color='red', alpha=0.3, label='Inflammatory', linewidth=4)
sns.kdeplot(data=data, x='mcsteps', weights='Remodeling', fill=True, color='springgreen', alpha=0.3, label='Remodeling', linewidth=4)
sns.kdeplot(data=data, x='mcsteps', weights='Anti-inflammatory', fill=True, color='darkblue', alpha=0.3, label='Anti-inflammatory', linewidth=4)

# Add labels and title
plt.xlabel('MC Steps', fontsize=14)
# plt.ylabel('Total Number of Cells', fontsize=14)
# plt.title('Density Plot of Cell Populations Over MC Steps', fontsize=16)

# Ensure the plot starts at mcsteps = 0
plt.xlim(0, data['mcsteps'].max())

# Add legend outside the plot
plt.legend(title="Cell Type", fontsize=12, bbox_to_anchor=(1.05, 1), loc='upper left')

# Add gridlines for better readability
# plt.grid(True, linestyle="--", linewidth=0.5)

# Remove upper and right spines
sns.despine()

# Show the plot
plt.tight_layout()
plt.savefig("Benchmark_results/density_cell_plot.png", dpi=400, transparent=True)
plt.show()
