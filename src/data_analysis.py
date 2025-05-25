import os, sys, argparse
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

    # Generate QQ plots (for normality checks)
    task_time_qq_plot = statistical_tools.generate_qq_plots(df_long.copy(), 'time', data_dir=data_directory)
    task_error_qq_plot = statistical_tools.generate_qq_plots(df_long.copy(), 'error', data_dir=data_directory)

    # Statistical tests
    task_time_results = statistical_tools.compute_repeated_measures(df_long.copy(), 'time')
    task_error_results = statistical_tools.compute_repeated_measures(df_long.copy(), 'error')

    # Combine and save results
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
else:
    raise ImportError("This script is intended to be run directly, not imported as a module.")
