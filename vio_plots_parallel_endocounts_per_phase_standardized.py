import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from the CSV file
data_file = os.path.join('Parallel_results', 'parallel_snellius_endocount_processors.csv')

# Check if the file exists
if not os.path.exists(data_file):
    raise FileNotFoundError(f"File not found: {data_file}")

data = pd.read_csv(data_file)

# Create the results folder if it doesn't exist
results_folder = 'Parallel_results'
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

# Set Seaborn style for better aesthetics
sns.set_theme(style="whitegrid")

# Define the phases for plotting
phases = ['IP_h', 'PP_h', 'RP_h']

# Create a figure for all violin plots with enough width for individual plots
fig, axes = plt.subplots(1, len(phases), figsize=(18, 6), sharex=True, sharey=True)  # Keep original size

# Adjust spacing between subplots to make them closer without squishing
plt.subplots_adjust(wspace=0.05)  # Reduce horizontal space between plots

# Iterate over each phase and create a violin plot
for i, phase in enumerate(phases):
    ax = axes[i]
    
    # Create a color palette based on IP_h (simulation time)
    colors = sns.color_palette("coolwarm", 7)  # Generate a discrete color palette
    
    # Create a violin plot with density_norm and custom palette
    sns.violinplot(
        x='Endothelial Count',
        y=phase,
        data=data,
        ax=ax,
        inner=None,  # Disable internal lines so we can add custom mean lines
        palette=colors,  # Use discrete list of colors
        legend=False  # Avoid redundant legends
    )
    
    # Overlay mean lines with linewidth=4 on each violin
    means = data.groupby('Endothelial Count')[phase].mean()
    for j, mean in enumerate(means):
        ax.plot([j - 0.2, j + 0.2], [mean, mean], color='black', linewidth=4)  # Add thick mean line
    
    # Add a title for each subplot indicating the phase
    ax.set_title(f'{phase}', fontsize=14)
    
    # Customize y-axis range for consistency across all plots
    # ax.set_ylim(0.2, 1.4)
    
    # Add a horizontal cutoff line at y=0.8
    ax.axhline(y=0.8, color='red', linestyle='--', linewidth=1.5)
    
    # Set x-axis label only for the last subplot
    if i == len(phases) - 1:
        ax.set_xlabel('Endothelial Count', fontsize=12)
    
    # Set y-axis label only for the first subplot
    if i == 0:
        ax.set_ylabel('Values', fontsize=12)
    
    # Customize y-axis ticks: Keep regular intervals below 0.8 and larger intervals above it
    # lower_ticks = [0.2, 0.4, 0.6, 0.8]  # Ticks below or at 0.8
    # upper_ticks = [1.0, 1.4, 1.8, 2.2, 2.4]   # Ticks above 0.8 with larger intervals
    # ax.set_yticks(lower_ticks + upper_ticks)
    
    # Remove upper and right spines to clean up the plot appearance
    sns.despine(ax=ax)

# Save the combined plot as a PNG file in the Parallel_results folder
output_file = os.path.join(results_folder, 'combined_violin_plot_phases_endocounts.png')
plt.savefig(output_file, dpi=300)  # High-resolution output

print(f"Saved {output_file}")

# Display the plot (optional)
plt.show()
