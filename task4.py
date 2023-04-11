import task1, task3, json
import pandas as pd
import matplotlib.pyplot as plt
import re

# Helper function to set subplots on figure 1
def plot_bar(ax, df, col_1, title_):
    ax.bar(data=df, x='Words', height='freq', color = col_1)
    ax.set_title(title_)
    ax.tick_params(axis='x', rotation=90)
    ax.set_xlabel('Words')
    ax.set_ylabel('frequency')

    for label, rect in enumerate(ax.patches):
        height = rect.get_height()
        ax.text(
            rect.get_x() + rect.get_width() / 2, 
            height,
            df['freq'][label], 
            ha="center", 
            va="bottom",
            rotation=0, 
            fontsize=12,
            bbox = dict(facecolor = 'whitesmoke', alpha =.8)
        )
    return ax

# Helper function to plot the comparison image
def comparison_plot(topW_0, topW_1, output_plot_filename, starting_links):
    plt.rcParams['figure.figsize'] = [20,8]
    plt.rc('font', size = 15)

    fig, (ax1, ax2) = plt.subplots(1, 2) 
    fig.suptitle('top 10 most common words in each seed_url') 
    ax1 = plot_bar(ax1, topW_0, 'tab:blue', re.sub('http://115.146.93.142/samplewiki/', '', starting_links[0]))
    ax2 = plot_bar(ax2, topW_1, 'skyblue', re.sub('http://115.146.93.142/samplewiki/', '', starting_links[1]))

    plt.savefig(output_plot_filename, bbox_inches='tight')
    plt.show()

    # Task 4 - Plotting the Most Common Words (2 Marks)
def task4(bow, output_plot_filename):
    # The bow dataframe is the output of Task 3, it has 
    # three columns, link_url, words and seed_url. The 
    # output plot should show which words are most common
    # for each seed_url. The visualisation is your choice,
    # but you should make sure it makes sense for what it
    # is meant to be.
    # Implement Task 4 here
    top_words = {}

    starting_links = sorted(bow['seed_url'].unique())

    def get_top_words(starting_link, df):
        words_list = []
        [words_list.extend(list.split()) for list in bow[bow['seed_url']==starting_link]['words']]
        df = pd.Series(words_list).value_counts()[:10].reset_index()
        df.columns = ['Words', 'freq']
        return df

    topW_0 = get_top_words(starting_links[0], bow)
    topW_1 = get_top_words(starting_links[1], bow)

    # Create comparison plot
    comparison_plot(topW_0, topW_1, output_plot_filename, starting_links)

    top_words[starting_links[0]] = list(topW_0['Words'].values)
    top_words[starting_links[1]] = list(topW_1['Words'].values)
    return top_words