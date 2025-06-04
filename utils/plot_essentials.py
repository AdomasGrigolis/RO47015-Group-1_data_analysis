import os, sys
import seaborn as sns
import matplotlib.pyplot as plt
from statannotations.Annotator import Annotator

def boxplot(data, measure, config, data_dir, annotations_dict=None, unique_id=0):
    order = config.get('order', ['0', '1', '2'])
    title = config.get('title', f'Boxplot of {measure}')
    x_label = config.get('x_label', measure)
    y_label = config.get('y_label', 'Condition')
    palette = config.get('palette', 'Set2')
    y_lim = config.get('y_lim', None)

    file_title = title.replace(" ", "_") + "_" + str(unique_id)
    directory = os.path.join(data_dir, 'plots')

    plt.figure(figsize=(10, 6))
    ax = sns.boxplot(
        data=data,
        x=measure,
        y='condition',
        palette=palette,
        orient='h',
        whis=[0, 100],
        flierprops={"marker": "x", "markersize": 5},
        order=order
    )
    sns.stripplot(
        data=data,
        x=measure,
        y='condition',
        color='black',
        size=3,
        jitter=True,
        dodge=True,
        alpha=0.5,
        ax=ax,
        order=order
    )

    # statannotations
    if annotations_dict and hasattr(ax, 'annotate'):
        present_conditions = set(data['condition'].unique())
        pairs = [p for p in annotations_dict.keys() if p[0] in present_conditions and p[1] in present_conditions]
        annotations = [annotations_dict[p] for p in pairs]
        annotator = Annotator(ax, pairs, data=data, x=measure, y='condition', order=order, orient='h')
        annotator.configure(test=None, text_format='star')
        annotator.set_custom_annotations(annotations)
        annotator.annotate()

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    if y_lim:
        ax.set_xlim(y_lim)

    if 'condition_labels' in config:
        ax.set_yticklabels([config['condition_labels'].get(str(l), str(l)) for l in ax.get_yticks()])
    plt.tight_layout()

    # Save plot
    if not os.path.exists(directory):
        os.makedirs(directory)
    plt.savefig(f'{directory}/{file_title}.jpg', format='jpeg', dpi=600)
    plt.close()

def plot_learning_curve(data, measure, data_dir, config, unique_id=0):
    order = config.get('order', ['0', '1', '2'])
    title = config.get('title', f'Learning Curve: {measure}')
    y_label = config.get('y_label', measure)
    x_label = config.get('x_label', 'Trial')
    palette = config.get('palette', 'Set2')
    invert_yaxis = config.get('invert_yaxis', False)
    file_title = title.replace(" ", "_") + "_" + str(unique_id)
    directory = os.path.join(data_dir, 'plots')

    data = data.copy()
    data = data[data['trialID'].notna()]
    data['trialID'] = data['trialID'].astype(int)

    plt.figure(figsize=(8, 5))
    ax = sns.lineplot(
        data=data,
        x='trialID',
        y=measure,
        marker='o',
        hue='condition',
        palette=palette,
        errorbar='se'
    )
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks([1, 2, 3])
    if invert_yaxis:
        plt.gca().invert_yaxis()
    plt.tight_layout()

    if 'condition_labels' in config:
        handles, labels = ax.get_legend_handles_labels()
        # Convert all labels to string for matching
        label_to_handle = {str(l): h for h, l in zip(handles, labels)}
        # Reorder handles and labels according to order
        ordered_handles = [label_to_handle[o] for o in order if o in label_to_handle]
        ordered_labels = [config['condition_labels'].get(o, o) for o in order if o in label_to_handle]
        ax.legend(ordered_handles, ordered_labels, title='condition')

    if not os.path.exists(directory):
        os.makedirs(directory)
    plt.savefig(f'{directory}/{file_title}.jpg', format='jpeg', dpi=600)
    plt.close()
