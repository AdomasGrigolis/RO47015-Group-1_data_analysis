import argparse
from utils import parse_core, statistical_tools, annotations, plot_essentials
from cfg import plot_config

# Main function to handle user input and call relevant processing functions
if __name__ == '__main__':
    print("Hello! This is the data analysis script.")
    # Argument parsing
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-d", "--directory", default="./data", help="Main data directory")
    args = arg_parser.parse_args()
    data_directory = args.directory

    df_long = parse_core.parse_data(data_directory)

    # Shapiro-Wilk tests for normality
    task_time_normality_cond = statistical_tools.check_normality_condition(df_long.copy(), 'time', alpha=0.05, data_dir=data_directory)
    task_error_normality_cond = statistical_tools.check_normality_condition(df_long.copy(), 'error', alpha=0.05, data_dir=data_directory)
    task_time_normality_res = statistical_tools.check_normality_residuals(df_long.copy(), 'time', alpha=0.05, data_dir=data_directory)
    task_error_normality_res = statistical_tools.check_normality_residuals(df_long.copy(), 'error', alpha=0.05, data_dir=data_directory)

    # Statistical tests
    task_time_results = statistical_tools.compute_repeated_measures(df_long.copy(), 'time', parametric=False)
    task_error_results = statistical_tools.compute_repeated_measures(df_long.copy(), 'error', parametric=False)
    learning_time_results = statistical_tools.learning_curve(df_long.copy(), 'time')
    learning_error_results = statistical_tools.learning_curve(df_long.copy(), 'error')

    # Combine and save results
    task_time_results['normality_res'] = task_time_normality_res
    task_error_results['normality_res'] = task_error_normality_res
    task_time_results['normality_cond'] = task_time_normality_cond
    task_error_results['normality_cond'] = task_error_normality_cond
    task_time_results['learning_curve'] = learning_time_results
    task_error_results['learning_curve'] = learning_error_results
    results_dict = {
        'time': task_time_results,
        'error': task_error_results
    }
    statistical_tools.save_results_to_excel(results_dict, data_dir=data_directory)

    # Create annotations for plotting annotator
    task_time_annotations = annotations.extract_condition_annotations(results_dict['time'])
    task_error_annotations = annotations.extract_condition_annotations(results_dict['error'])

    # Plotting
    plot_essentials.boxplot(df_long.copy(), 'time', plot_config.boxplot_config_time, data_directory, annotations_dict=task_time_annotations, unique_id=0)
    plot_essentials.boxplot(df_long.copy(), 'error', plot_config.boxplot_config_error, data_directory, annotations_dict=task_error_annotations, unique_id=0)
    plot_essentials.plot_learning_curve(df_long.copy(), 'time', data_directory, plot_config.learning_curve_config_time)
    plot_essentials.plot_learning_curve(df_long.copy(), 'error', data_directory, plot_config.learning_curve_config_error)
else:
    raise ImportError("This script is intended to be run directly, not imported as a module.")
