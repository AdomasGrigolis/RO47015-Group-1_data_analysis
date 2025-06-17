import os
import pandas as pd
import pingouin as pg
import matplotlib.pyplot as plt
import scipy.stats as stats
from statsmodels.formula.api import ols
from cfg.plot_config import condition_labels
import statsmodels.formula.api as smf

def compute_repeated_measures(df_long, measure, parametric=False):
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
        parametric=parametric
    )

    group_stats = df_long.groupby('condition')[measure].agg(['mean', 'std']).reset_index()

    return {
        'stat_analysis': friedman,
        'results': pairwise,
        'test': 'friedman + non-parametric pairwise',
        'group_stats': group_stats
    }

def learning_curve(df_long, measure):
    df_long['condition'] = df_long['condition'].astype(str).astype('category')
    df_long['condition'] = df_long['condition'].cat.reorder_categories(
        ['0', '1', '2'], ordered=True
    )
    df_long['trialID'] = df_long['trialID'].astype(str).astype('category')
    df_long['trialID'] = df_long['trialID'].cat.set_categories(['1', '2', '3'], ordered=True)

    model = smf.mixedlm(
        formula=f"{measure} ~ trialID * condition",
        data=df_long,
        groups=df_long["participantID"],
        re_formula="~trialID"
    )

    results = model.fit()

    table_df = results.summary().tables[1]
    
    if not table_df.index.empty and table_df.index[0] != 0:
        df = table_df.copy()
        df.index.name = 'variable'
    else:
        print("Warning: could not save LM results with variable names.")
        return table_df
    
    # Convert numeric columns
    numeric_cols = df.select_dtypes(include=['object']).columns
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='ignore')
    return df.reset_index()

def generate_qq_plot_residuals(residuals, measure_name, data_dir=os.path.join(os.getcwd(), 'data')):
    plot_dir = os.path.join(data_dir, 'plots')
    if plot_dir:
        os.makedirs(plot_dir, exist_ok=True)
    
    fig = plt.figure(figsize=(6, 6))
    stats.probplot(residuals, dist="norm", plot=plt)
    plt.title(f"QQ Plot for residuals of {measure_name}")
    plt.tight_layout()
    
    plot_path = os.path.join(plot_dir, f"qqplot_residuals_{measure_name}.png")
    plt.savefig(plot_path)
    plt.close(fig)
    
    return plot_path

def check_normality_residuals(df_long, measure, alpha=0.01, data_dir=os.path.join(os.getcwd(), 'data')):
    model = ols(f'{measure} ~ C(condition) + C(participantID)', data=df_long).fit()
    residuals = model.resid
    qq_plot_path = generate_qq_plot_residuals(residuals, measure, data_dir=data_dir)
    normality = pg.normality(residuals, method='shapiro', alpha=alpha)
    return normality

def check_normality_condition(df_long, measure, alpha=0.01, pairs = [(0, 1), (0, 2), (1, 2)], data_dir=os.path.join(os.getcwd(), 'data')):
    plot_dir = os.path.join(data_dir, 'plots')
    os.makedirs(plot_dir, exist_ok=True)
    norm_results = []

    df_wide = df_long.pivot(index='participantID', columns='condition', values=measure)
    df_wide.columns = [f'cond_{col}' for col in df_wide.columns]

    for cond1, cond2 in pairs:
        col1 = f'cond_{cond1}'
        col2 = f'cond_{cond2}'
        
        # Calculate difference scores
        diffs = df_wide[col1] - df_wide[col2]
        
        # Test normality of difference scores
        norm_test = pg.normality(diffs, method='shapiro', alpha=alpha)
        norm_test.insert(0, 'condition_pair', f"{cond1}-{cond2}")
        norm_results.append(norm_test)

        label1 = condition_labels.get(col1, col1) if condition_labels else col1
        label2 = condition_labels.get(col2, col2) if condition_labels else col2
        fig = plt.figure(figsize=(6, 6))
        stats.probplot(diffs, dist="norm", plot=plt)
        plt.title(f"QQ Plot of {label1} - {label2} {measure}")
        plt.tight_layout()
        plot_path = os.path.join(plot_dir, f"qqplot_diff_{col1}_vs_{col2}_{measure}.png")
        plt.savefig(plot_path)
        plt.close(fig)

    norm_results_df = pd.concat(norm_results, ignore_index=True)
    return norm_results_df

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
            # Save learning curve results
            if 'learning_curve' in result and isinstance(result['learning_curve'], pd.DataFrame):
                result['learning_curve'].to_excel(writer, sheet_name=f"{label}_learning_curve", index=False)
                metadata.append({'Label': label, 'Test': 'Learning Curve', 'Sheet': f"{label}_learning_curve"})
            # Save group stats
            if 'group_stats' in result and isinstance(result['group_stats'], pd.DataFrame):
                result['group_stats'].to_excel(writer, sheet_name=f"{label}_group_stats", index=False)
                metadata.append({'Label': label, 'Test': 'Group Stats', 'Sheet': f"{label}_group_stats"})
            # Save normality results
            if 'normality_res' in result and isinstance(result['normality_res'], pd.DataFrame):
                result['normality_res'] = result['normality_res'].reset_index()
                result['normality_res'].to_excel(writer, sheet_name=f"{label}_normality_residuals", index=False)
                metadata.append({'Label': label, 'Test': 'Normality of residuals', 'Sheet': f"{label}_normality_residuals"})
            if 'normality_cond' in result and isinstance(result['normality_cond'], pd.DataFrame):
                result['normality_cond'] = result['normality_cond'].reset_index()
                result['normality_cond'].to_excel(writer, sheet_name=f"{label}_normality_condition", index=False)
                metadata.append({'Label': label, 'Test': 'Normality of condition', 'Sheet': f"{label}_normality_condition"})
        # Save metadata
        if metadata:
            pd.DataFrame(metadata).to_excel(writer, sheet_name="Metadata", index=False)
        else:
            pd.DataFrame({'Message': ['No results available']}).to_excel(writer, sheet_name="Empty", index=False)
