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
fig, axes = plt.subplots(1, len(phases), figsize=(18, 6), sharey=True)

# Adjust spacing between subplots to make them closer without squishing
plt.subplots_adjust(wspace=0.05)

# Iterate over each phase and create a violin plot
for i, phase in enumerate(phases):
    ax = axes[i]
    
    # Create a violin plot with Processor Number as hue and custom palette
    sns.violinplot(
        x='Endothelial Count',
        y=phase,
        hue='Processor Number',
        data=data,
        ax=ax,
        inner=None,  # Disable internal lines so we can add custom mean lines
        palette="coolwarm",  # Use your specified color scheme
        dodge=True  # Separate violins by hue within each x category
    )
    
    # Overlay mean lines for each combination of Endothelial Count and Processor Number
    means = data.groupby(['Endothelial Count', 'Processor Number'])[phase].mean().reset_index()
    for _, row in means.iterrows():
        x_pos = list(data['Endothelial Count'].unique()).index(row['Endothelial Count'])
        ax.plot(
            [x_pos - 0.2, x_pos + 0.2],  # Adjust position slightly for separation
            [row[phase], row[phase]],
            color='black',
            linewidth=4,
        )
    
    # Add a title for each subplot indicating the phase
    ax.set_title(f'{phase}', fontsize=14)
    
    # Customize y-axis range for consistency across all plots
    ax.axhline(y=0.8, color='red', linestyle='--', linewidth=1.5)  # Add cutoff line
    
    # Rotate x-axis labels for better readability
    ax.tick_params(axis='x', rotation=45)
    
    # Set x-axis label only for the last subplot
    if i == len(phases) - 1:
        ax.set_xlabel('Endothelial Count', fontsize=12)
    
    # Set y-axis label only for the first subplot
    if i == 0:
        ax.set_ylabel('Hours', fontsize=12)

sns.despine()

# Save the combined plot as a PNG file in the Parallel_results folder
output_file = os.path.join(results_folder, 'combined_violin_plot_phases_endocounts_parallel.png')
plt.savefig(output_file, dpi=300)  # High-resolution output

print(f"Saved {output_file}")

# Display the plot (optional)
plt.show()
