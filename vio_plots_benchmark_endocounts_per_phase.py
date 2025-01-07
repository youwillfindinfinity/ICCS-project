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
phases = ['PP_h', 'RP_h', 'IP_h']

# Normalize IP_h values to use as the color gradient
data['Color Intensity'] = data['IP_h'] / data['IP_h'].max()

# Create violin plots for each phase
for phase in phases:
    plt.figure(figsize=(10, 6))
    
    # Create a color palette based on IP_h (simulation time)
    cmap = sns.color_palette("coolwarm", as_cmap=True)
    norm = plt.Normalize(vmin=data['IP_h'].min(), vmax=data['IP_h'].max())
    colors = cmap(norm(data['IP_h']).data).tolist()  # Convert NumPy array to list
    
    # Create a violin plot with density_norm and custom palette
    ax = sns.violinplot(
        x='Endothelial Count', 
        y=phase, 
        data=data, 
        density_norm='width',  # Updated parameter name
        inner=None,  # Disable internal lines so we can add custom mean lines
        palette=colors,  # Use converted list of colors
        legend=False  # Avoid redundant legends
    )
    
    # Overlay mean lines with linewidth=4 on each violin
    means = data.groupby('Endothelial Count')[phase].mean()
    for i, mean in enumerate(means):
        ax.plot([i - 0.2, i + 0.2], [mean, mean], color='black', linewidth=4, label='Mean' if i == 0 else "")  # Add thick mean line
    
    # Add a colorbar to indicate simulation time intensity (IP_h)
    sm = plt.cm.ScalarMappable(cmap="coolwarm", norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=plt.gca())  # Explicitly link colorbar to current axes
    cbar.set_label('Simulation Time (in hours)', fontsize=12)
    
    # Customize the plot with titles and labels
    plt.title(f'Violin Plot for {phase}', fontsize=16)
    plt.xlabel('Endothelial Count', fontsize=14)
    plt.ylabel(f'{phase} Values', fontsize=14)
    
    # Save the plot as a PNG file in the Benchmark_results folder
    output_file = os.path.join(results_folder, f'{phase}_violin_plot_phases_endocounts.png')
    plt.savefig(output_file, dpi=300)  # High-resolution output
    
    print(f"Saved {output_file}")
    
    # Close the plot to avoid overlapping figures in subsequent iterations
    plt.close()
