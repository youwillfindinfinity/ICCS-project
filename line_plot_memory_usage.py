import pandas as pd
import matplotlib.pyplot as plt

# Read the combined data from the CSV file
csv_file = results_folder = 'Benchmark_results' + "/" + "benchmark_combined_memory_usage.csv"
df = pd.read_csv(csv_file)

# Example list of endothelial counts (used to map Index to Endothelial Count)
endothelial_counts = [
    10, 10, 10, 10, 10,
    100, 100,100, 100, 100,
    500, 500, 500, 500, 500,
    1000, 1000,1000, 1000, 1000,
    2000, 2000, 2000, 2000, 2000,
    3000, 3000, 3000, 3000, 3000,
    4000, 4000, 4000, 4000, 4000,
    5000, 5000, 5000, 5000, 5000
]

# Map Index to Endothelial Count
df['Endothelial Count'] = df['Index'].map(lambda x: endothelial_counts[x])

# Group data by Endothelial Count and MCS
grouped = df.groupby(['Endothelial Count', 'MCS'])

# Aggregate data: calculate mean, min, and max of Memory (MB)
agg_data = grouped['Memory (MB)'].agg(['mean', 'min', 'max']).reset_index()

# Plotting
plt.figure(figsize=(12, 4))

# Get unique endothelial counts
unique_counts = sorted(df['Endothelial Count'].unique())

# Loop through each unique endothelial count to plot lines with fill_between
for count in unique_counts:
    subset = agg_data[agg_data['Endothelial Count'] == count]
    
    # Extract MCS values and corresponding statistics
    mcs_values = subset['MCS']
    mean_memory = subset['mean']
    min_memory = subset['min']
    max_memory = subset['max']
    
    # Plot mean line with fill_between for min/max range
    plt.plot(mcs_values, mean_memory, label=f'Endothelial Count: {count}')
    plt.fill_between(mcs_values, min_memory, max_memory, alpha=0.2)

# Customize plot
plt.title('Memory Usage Over MCS for Different Endothelial Counts')
plt.xlabel('Monte Carlo Steps (MCS)')
plt.ylabel('Memory Usage (MB)')
plt.ylim([1.5e3, 2.8e3])
# plt.xlim([0, 50000])
# plt.xscale('log')
plt.yscale('log')
# plt.legend(loc='lower right')
plt.grid(True)
plt.tight_layout()

# Show plot
plt.show()
