import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Load data from the provided file paths
parallel_data = pd.read_csv("Parallel_results/snellius_processor_nr_exp.csv")
benchmark_data = pd.read_csv("Benchmark_results/processor_nr_exp.csv")

# Group data by processor number and calculate mean and standard deviation for each dataset
parallel_stats = parallel_data.groupby("Processor nr")["Total sim time"].agg(["mean", "std"]).reset_index()
benchmark_stats = benchmark_data.groupby("Processor nr")["Total sim time"].agg(["mean", "std"]).reset_index()

# Plotting with seaborn
plt.figure(figsize=(20, 6))
sns.set(style="whitegrid")

# Parallel data line with fill between for error
plt.plot(parallel_stats["Processor nr"], parallel_stats["mean"], label="Parallel (128 CC3D Processors)", marker="o", linewidth = 4, color = 'red')
plt.fill_between(parallel_stats["Processor nr"], 
                 parallel_stats["mean"] - parallel_stats["std"], 
                 parallel_stats["mean"] + parallel_stats["std"], 
                 alpha=0.3, color = 'red')

# Benchmark data line with fill between for error
plt.plot(benchmark_stats["Processor nr"], benchmark_stats["mean"], label="Benchmark (No MPI Parallelization)", marker="o", linewidth = 4, color = 'blue')
plt.fill_between(benchmark_stats["Processor nr"], 
                 benchmark_stats["mean"] - benchmark_stats["std"], 
                 benchmark_stats["mean"] + benchmark_stats["std"], 
                 alpha=0.3, color = 'blue')

# Highlight optimal processor numbers
plt.axvline(x=4, color="red", linestyle="--", label="Optimal Processor Count (MPI)", linewidth = 4)
plt.axvline(x=16, color="blue", linestyle="--", label="Optimal Processor Count (CC3D)", linewidth = 4)
# Add legend outside the plot
plt.legend(title="", fontsize=12, bbox_to_anchor=(1.05, 1), loc='upper left')
# Add labels, legend, and title
# plt.xlabel("Number of Processors")
# plt.ylabel("Total Simulation Time (hours)")
# plt.title("Simulation Time vs Processor Number")
plt.tight_layout()
sns.despine()

results_folder = 'Benchmark_results'
output_file = os.path.join(results_folder, 'benchmark_parallel_analysis.png')
plt.savefig(output_file, dpi=300)  # High-resolution output

# Show plot
plt.show()
