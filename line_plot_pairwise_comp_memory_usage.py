import pandas as pd
import matplotlib.pyplot as plt

# Read the combined data from the CSV file
results_folder = 'Benchmark_results'
csv_file = results_folder + "/" + "combined_memory_usage.csv"
df = pd.read_csv(csv_file)

# Example list of endothelial counts (used to map Index to Endothelial Count)
endothelial_counts = [
    10, 10,
    100, 100,
    500, 500, 
    1000, 1000,
    2000, 2000, 
    3000, 3000, 
    4000, 4000,
    5000, 5000,
]

# Map Index to Endothelial Count
df['Endothelial Count'] = df['Index'].map(lambda x: endothelial_counts[x])

# Function to plot specific pairs of endothelial counts
def plot_specific_pairs(df, counts_to_compare):
    """
    Plots memory usage over MCS for specific pairs of endothelial counts.
    
    Parameters:
        df (pd.DataFrame): The data frame containing memory usage data.
        counts_to_compare (list): List of specific endothelial counts to compare.
    """
    # Filter the DataFrame for the specified endothelial counts
    filtered_df = df[df['Endothelial Count'].isin(counts_to_compare)]
    
    # Group data by Endothelial Count and MCS
    grouped = filtered_df.groupby(['Endothelial Count', 'MCS'])

    # Aggregate data: calculate mean, min, and max of Memory (MB)
    agg_data = grouped['Memory (MB)'].agg(['mean', 'min', 'max']).reset_index()

    # Plotting
    plt.figure(figsize=(6, 3))

    # Loop through each specified endothelial count to plot lines with fill_between
    for count in counts_to_compare:
        subset = agg_data[agg_data['Endothelial Count'] == count]
        
        # Extract MCS values and corresponding statistics
        mcs_values = subset['MCS']
        mean_memory = subset['mean']
        min_memory = subset['min']
        max_memory = subset['max']
        
        # Plot mean line with fill_between for min/max range
        plt.plot(mcs_values, mean_memory, label=f'Endothelial Count: {count}', linewidth = 3)
        plt.fill_between(mcs_values, min_memory, max_memory, alpha=0.2)

    # Customize y-axis ticks
    ticks_before_2200 = list(range(0, 2201, 1200))  # Ticks from 0 to 2200 with step of 1200
    ticks_after_2200 = list(range(2250, int(agg_data['max'].max()) + 1, 100))  # Ticks after 2200 with step of 50
    all_ticks = ticks_before_2200 + ticks_after_2200

    plt.yticks(all_ticks)  # Set custom y-axis ticks

    # Customize plot
    plt.title('Memory Usage Over MCS for Selected Endothelial Counts')
    plt.xlabel('Monte Carlo Steps (MCS)')
    plt.ylabel('Memory Usage (MB)')
    plt.ylim([1200, 2900])
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Show plot
    plt.show()


# Call the function to plot specific pairs (e.g., 1000 and 5000)
plot_specific_pairs(df, [1000, 5000])
