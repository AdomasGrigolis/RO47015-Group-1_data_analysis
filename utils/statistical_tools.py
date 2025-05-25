import os
import pandas as pd
import pingouin as pg
import matplotlib.pyplot as plt
import scipy.stats as stats

def compute_repeated_measures(df_long, measure):
    friedman = pg.friedman(
        data=df_long,
        dv=measure,
        within='condition',
        subject='participantID'
    )

    pairwise = pg.pairwise_tests(
        data=df_long,
        dv=measure,
        within='condition',
        subject='participantID',
        padjust='holm',
        alternative='two-sided',
        parametric=False
    )

    return {
        'test': 'friedman + non-parametric pairwise',
        'stat_analysis': friedman,
        'results': pairwise
    }

def generate_qq_plots(data, measure, groupby_col='condition', data_dir=os.path.join(os.getcwd(), 'data')):
    plot_dir = os.path.join(data_dir, 'plots')
    figures_or_paths = {}
    if plot_dir:
        os.makedirs(plot_dir, exist_ok=True)
    for group_level in data[groupby_col].unique():
        subset = data[data[groupby_col] == group_level][measure]
        fig = plt.figure(figsize=(6, 6))
        stats.probplot(subset, dist="norm", plot=plt)
        plt.title(f"QQ Plot for {groupby_col} {group_level} - {measure}")
        plt.tight_layout()
        if plot_dir:
            plot_path = os.path.join(plot_dir, f"qqplot_{groupby_col}_{group_level}_{measure}.png")
            plt.savefig(plot_path)
            figures_or_paths[group_level] = plot_path
        else:
            figures_or_paths[group_level] = fig
        plt.close(fig)
    return figures_or_paths

def save_results_to_excel(results_dict, data_dir=os.path.join(os.getcwd(), 'data')):
    results_dir = os.path.join(data_dir, 'results')
    os.makedirs(results_dir, exist_ok=True)
    save_path = os.path.join(results_dir, "results_summary.xlsx")
    with pd.ExcelWriter(save_path, mode='w') as writer:
        metadata = []
        for label, result in results_dict.items():
            # Save main test (Friedman)
            if 'stat_analysis' in result and isinstance(result['stat_analysis'], pd.DataFrame):
                result['stat_analysis'].to_excel(writer, sheet_name=f"{label}_friedman", index=False)
                metadata.append({'Label': label, 'Test': 'Friedman', 'Sheet': f"{label}_friedman"})
            # Save pairwise tests
            if 'results' in result and isinstance(result['results'], pd.DataFrame):
                result['results'].to_excel(writer, sheet_name=f"{label}_pairwise", index=False)
                metadata.append({'Label': label, 'Test': 'Pairwise', 'Sheet': f"{label}_pairwise"})
        # Save metadata
        if metadata:
            pd.DataFrame(metadata).to_excel(writer, sheet_name="Metadata", index=False)
        else:
            pd.DataFrame({'Message': ['No results available']}).to_excel(writer, sheet_name="Empty", index=False)