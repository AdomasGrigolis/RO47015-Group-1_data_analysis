# Universal configuration for plotting
palette = 'Set2'

# Condition remapping
condition_mapping = {
        '0': 'Baseline',
        '1': 'Visual Assistance',
        '2': 'Haptic Guidance'
}

condition_labels = {
    'cond_0': 'Baseline',
    'cond_1': 'Visual',
    'cond_2': 'Haptic'
}

boxplot_config_time = {
    'title': 'Completion Time by Condition',
    'x_label': 'time (s)',
    'y_label': 'Condition',
    'palette': palette,
    'y_lim': None,
    'condition_labels': condition_mapping
}
boxplot_config_error = {
    'title': 'Path following MSE by Condition',
    'x_label': 'mse (m^2)',
    'y_label': 'Condition',
    'palette': palette,
    'y_lim': None,
    'condition_labels': condition_mapping
}

learning_curve_config_time = {
    'title': 'Completion Time Learning Curve',
    'x_label': 'Trial number',
    'y_label': 'time (s)',
    'palette': palette,
    'invert_yaxis': False,
    'condition_labels': condition_mapping
}

learning_curve_config_error = {
    'title': 'Path following MSE Learning Curve',
    'x_label': 'Trial number',
    'y_label': 'mse (m^2)',
    'palette': palette,
    'invert_yaxis': False,
    'condition_labels': condition_mapping
}
