import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from the cellcount.txt file
data_file = 'ICCS_experiments/pc_endothelial_benchmarkWholeData/datafiles/cellcount.txt'  # Update this path if necessary
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

# Normalize weights (densities) so that y-axis values are between 0 and 1
total_cells_per_step = data[['Neutral', 'Inflammatory', 'Remodeling', 'Anti-inflammatory']].sum(axis=1)
data['Neutral'] /= total_cells_per_step
data['Inflammatory'] /= total_cells_per_step
data['Remodeling'] /= total_cells_per_step
data['Anti-inflammatory'] /= total_cells_per_step

# Plot the line plot and fill the area under each line
plt.figure(figsize=(20, 4))  # Adjust figsize for better visualization

# Plot Neutral line and fill area
plt.plot(data['mcsteps'], data['Neutral'], color='black', label='Neutral', linewidth=2)
plt.fill_between(data['mcsteps'], data['Neutral'], color='black', alpha=0.3)

# Plot Inflammatory line and fill area
plt.plot(data['mcsteps'], data['Inflammatory'], color='red', label='Inflammatory', linewidth=2)
plt.fill_between(data['mcsteps'], data['Inflammatory'], color='red', alpha=0.3)

# Plot Remodeling line and fill area
plt.plot(data['mcsteps'], data['Remodeling'], color='springgreen', label='Remodeling', linewidth=2)
plt.fill_between(data['mcsteps'], data['Remodeling'], color='springgreen', alpha=0.3)

# Plot Anti-inflammatory line and fill area
plt.plot(data['mcsteps'], data['Anti-inflammatory'], color='darkblue', label='Anti-inflammatory', linewidth=2)
plt.fill_between(data['mcsteps'], data['Anti-inflammatory'], color='darkblue', alpha=0.3)

# Add labels and title
plt.xlabel('MC Steps', fontsize=14)
plt.ylabel('Proportion (Normalized)', fontsize=14)
plt.title('Proportion of Cell Populations Over MC Steps (Normalized)', fontsize=16)

# Ensure the plot starts at mcsteps = 0
plt.xlim(0, data['mcsteps'].max())
plt.ylim(0, 1)  # Set y-axis range between 0 and 1

# Add legend outside the plot
plt.legend(title="Cell Type", fontsize=12, bbox_to_anchor=(1.05, 1), loc='upper left')



# Remove upper and right spines
sns.despine()

# Show and save the plot
plt.tight_layout()
plt.savefig("Benchmark_results/density_cell_plot.png", dpi=400, transparent=True)
plt.show()
