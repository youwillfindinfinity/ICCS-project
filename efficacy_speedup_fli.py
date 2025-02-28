import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# File path for the parallel dataset
parallel_file = "Parallel_results/eficalc_input_par_comp.csv"

# Load data
parallel_data = pd.read_csv(parallel_file)

# Filter data for processor numbers 1, 2, 4, and 8
processor_numbers = [1, 2, 4, 6, 8]
parallel_filtered = parallel_data[parallel_data["Processor nr"].isin(processor_numbers)]

# Treat the sequential run as the one with Processor nr = 1
sequential_time = parallel_filtered[parallel_filtered["Processor nr"] == 1].mean()

# Initialize dictionaries to store results
speedup = {}
parallel_efficiency = {}

phases = ["PP_h", "RP_h", "IP_h"]
phases_labels = ["PP", "RP", "IP"]
colors = {"PP_h": "gold", "RP_h": "lightgreen", "IP_h": "red"}

# Process data for each phase
for phase in phases:
    speedup[phase] = []
    parallel_efficiency[phase] = []

    for processor_nr in processor_numbers:
        # Get parallel time for the current processor number
        T_p_phase_mean = parallel_filtered.loc[parallel_filtered["Processor nr"] == processor_nr, phase].mean()
        T_s_phase = sequential_time[phase]  # Sequential time is the mean of Processor nr = 1

        # Speedup (S_p)
        S_p = T_s_phase / T_p_phase_mean if T_p_phase_mean > 0 else np.nan
        speedup[phase].append(S_p)

        # Parallel efficiency (E_p)
        E_p = S_p / processor_nr if S_p > 0 else np.nan
        parallel_efficiency[phase].append(E_p)

# Create a figure with subplots side by side (1 row, 3 columns)
fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharex=True)
fig.suptitle("Parallel Performance Metrics (Processor Numbers: 1, 2, 4, 6, 8)", fontsize=16)

# Plot computation time per phase with specific colors and standard deviation bars
for i in range(len(phases)):
    means = []
    stds = []
    for p in processor_numbers:
        phase_data = parallel_filtered.loc[parallel_filtered["Processor nr"] == p, phases[i]]
        means.append(phase_data.mean())
        stds.append(phase_data.std())

    axes[0].errorbar(processor_numbers, means, yerr=stds, label=f"{phases_labels[i]}", color=colors[phases[i]], linewidth=2)
axes[0].set_title("Computation Time (Hours)")
axes[0].set_ylabel("Time (hours)")


# Plot speedup per phase with specific colors
for i in range(len(phases)):
    axes[1].plot(processor_numbers, speedup[phases[i]], label=f"{phases_labels[i]}", color=colors[phases[i]], linewidth=2)
axes[1].set_title("Speedup ($S_p$)")
axes[1].set_ylabel("$S_p$")

# Plot parallel efficiency per phase with specific colors
for i in range(len(phases)):
    axes[2].plot(processor_numbers, np.array(parallel_efficiency[phases[i]]) * 100, label=f"{phases_labels[i]}", color=colors[phases[i]], linewidth=2)
axes[2].set_title("Parallel Efficiency ($E_p$)")
axes[2].set_ylabel("$E_p$ (%)")
axes[2].legend(title="", fontsize=12, bbox_to_anchor=(1.05, 1), loc='upper left')


# Shared x-axis label across all subplots
for ax in axes:
    ax.set_xlabel("Number of Processors ($P$)")
    sns.despine(ax=ax)


plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('parallel_performance_metrics.png', dpi=400)#, transparent=True)
plt.show()
