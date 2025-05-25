# Condition remapping
condition_mapping = {
        '0': 'Baseline',
        '1': 'Visual Guidance',
        '2': 'Haptic Guidance'
}

boxplot_config_time = {
    'title': 'Completion Time by Condition',
    'x_label': 'time (s)',
    'y_label': 'Condition',
    'palette': 'Set2',
    'y_lim': None,
    'condition_labels': condition_mapping
}
boxplot_config_error = {
    'title': 'Path following MSE by Condition',
    'x_label': 'mse (m^2)',
    'y_label': 'Condition',
    'palette': 'Set2',
    'y_lim': None,
    'condition_labels': condition_mapping
}