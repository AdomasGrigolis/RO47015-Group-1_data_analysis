import pandas as pd

def extract_condition_annotations(results, condition_pairs=None):
    if 'results' not in results or not isinstance(results['results'], pd.DataFrame):
        return {}

    pairwise_df = results['results']
    annotations = {}

    # If no pairs specified, use all unique pairs found in the results
    if condition_pairs is None:
        unique_conds = pd.unique(pairwise_df[['A', 'B']].values.ravel())
        condition_pairs = [(str(a), str(b)) for i, a in enumerate(unique_conds) for b in unique_conds[i+1:]]

    for a, b in condition_pairs:
        # Find the row for this pair (order-insensitive)
        row = pairwise_df[((pairwise_df['A'] == a) & (pairwise_df['B'] == b)) |
                          ((pairwise_df['A'] == b) & (pairwise_df['B'] == a))]
        if not row.empty:
            p_corr = row['p-corr'].iloc[0]
            annotation = (
                '****' if p_corr <= 1.00e-04 else
                '***' if p_corr <= 1.00e-03 else
                '**' if p_corr <= 1.00e-02 else
                '*' if p_corr <= 5.00e-02 else
                'ns'
            )
            annotations[(a, b)] = annotation
        else:
            annotations[(a, b)] = 'ns'
    return annotations