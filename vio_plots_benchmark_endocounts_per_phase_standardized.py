import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from the CSV file
data_file = r'Benchmark_results\endothelial_simulation_data_phases_endocounts.csv'
data = pd.read_csv(data_file)

# Create the results folder if it doesn't exist
results_folder = 'Benchmark_results'
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

# Set Seaborn style for better aesthetics
sns.set_theme(style="whitegrid")

# Define the phases for plotting
phases = ['IP_h', 'PP_h', 'RP_h']

# Normalize IP_h values to use as the color gradient
data['Color Intensity'] = data['RP_h'] / data['RP_h'].max()

# Create a figure for all violin plots
fig, axes = plt.subplots(1, len(phases), figsize=(18, 6), sharex=True, sharey=True)

# Iterate over each phase and create a violin plot
for i, phase in enumerate(phases):
    ax = axes[i]
    
    # Create a color palette based on IP_h (simulation time)
    cmap = sns.color_palette("coolwarm", as_cmap=True)
    norm = plt.Normalize(vmin=data['RP_h'].min(), vmax=data['RP_h'].max())
    colors = cmap(norm(data['RP_h']).data).tolist()  # Convert NumPy array to list

    # Create a violin plot with density_norm and custom palette
    sns.violinplot(
        x='Endothelial Count',
        y=phase,
        data=data,
        ax=ax,
        inner=None,  # Disable internal lines so we can add custom mean lines
        palette=colors,  # Use converted list of colors
        legend=False  # Avoid redundant legends
    )
    
    # Overlay mean lines with linewidth=4 on each violin
    means = data.groupby('Endothelial Count')[phase].mean()
    for j, mean in enumerate(means):
        ax.plot([j - 0.2, j + 0.2], [mean, mean], color='black', linewidth=4)  # Add thick mean line
    
    # Add a title for each subplot indicating the phase
    ax.set_title(f'{phase}', fontsize=14)
    
    # Customize y-axis range for consistency across all plots
    ax.set_ylim(0.2, 1.4)
    
    # Set x-axis label only for the last subplot
    if i == len(phases) - 1:
        ax.set_xlabel('Endothelial Count', fontsize=12)
    
    # Set y-axis label only for the first subplot
    if i == 0:
        ax.set_ylabel('Values', fontsize=12)

# Add a shared colorbar for all subplots to indicate simulation time intensity (IP_h)
sm = plt.cm.ScalarMappable(cmap="coolwarm", norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=axes.ravel().tolist(), orientation='horizontal', pad=0.1)
cbar.set_label('Simulation Time (in hours)', fontsize=12)

# Save the combined plot as a PNG file in the Benchmark_results folder
output_file = os.path.join(results_folder, 'combined_violin_plot_phases_endocounts.png')
plt.savefig(output_file, dpi=300)  # High-resolution output

print(f"Saved {output_file}")

# Display the plot (optional)
plt.show()
