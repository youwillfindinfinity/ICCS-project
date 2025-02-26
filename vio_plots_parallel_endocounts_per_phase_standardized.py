import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration
DATA_FILE = 'Parallel_results/parallel_snellius_endocount_processors.csv'
RESULTS_FOLDER = 'Parallel_results'

def main():
    # Verify data file exists
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(
            f"Data file not found at: {DATA_FILE}\n"
            "Please ensure:\n"
            "1. The file exists in the Parallel_results directory\n"
            "2. The filename matches exactly (case-sensitive)\n"
            "3. The file contains columns: Endothelial Count, Processor Number, IP_h, PP_h, RP_h"
        )

    # Load and validate data
    data = pd.read_csv(DATA_FILE)
    required_columns = {'Endothelial Count', 'IP_h', 'PP_h', 'RP_h'}
    if not required_columns.issubset(data.columns):
        missing = required_columns - set(data.columns)
        raise ValueError(f"Missing required columns: {missing}")

    # Create results directory
    os.makedirs(RESULTS_FOLDER, exist_ok=True)

    # Calculate total simulation time
    data['Total_h'] = data[['IP_h', 'PP_h', 'RP_h']].sum(axis=1)

    # Verify consistent data points per endothelial count
    counts = data.groupby('Endothelial Count').size()
    if not (counts == counts.iloc[0]).all():
        inconsistent = counts[counts != counts.iloc[0]].index.tolist()
        raise ValueError(f"Inconsistent data points for counts: {inconsistent}")

    # Prepare statistics
    stats = data.groupby('Endothelial Count')['Total_h'].agg(['mean', 'std']).reset_index()

    # Create visualization
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")
    
    plt.errorbar(
        x=stats['Endothelial Count'],
        y=stats['mean'],
        yerr=stats['std'],
        fmt='-o',
        color='#2ca02c',
        ecolor='#1f77b4',
        elinewidth=2,
        capsize=5,
        capthick=2
    )

    plt.title('Total Simulation Time by Endothelial Cell Count\n(Combined Phases with SD)', pad=15)
    plt.xlabel('Endothelial Cell Count', labelpad=10)
    plt.ylabel('Total Simulation Time (Hours) ± SD', labelpad=10)
    plt.xticks(stats['Endothelial Count'])
    plt.grid(True, alpha=0.3)

    # Save and show
    output_path = os.path.join(RESULTS_FOLDER, 'combined_simulation_time.png')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved combined visualization to: {output_path}")
    plt.show()

if __name__ == "__main__":
    main()
