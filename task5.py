from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns

# Helper Function to Send pca weights of interest to DF
def get_pca_df(component, pca, vocabulary):
    df = (pd.Series(        
        pca.components_[component], 
        index=vocabulary).sort_values(ascending=False)) 
    df = pd.concat([df[:10], df[-10:]]).reset_index()
    df.columns = ['tokens', 'weights']
    return df

# Helper function to set subplots on figure 1
def plot_bar(ax, df, col_1, col_2, title_):
    ax.bar(data=df[df['weights'] > 0], x='tokens', height='weights', color = col_1)
    ax.bar(data=df[df['weights'] <= 0], x='tokens', height='weights', color = col_2)
    ax.set_title(title_)
    ax.tick_params(axis='x', rotation=90)
    ax.set_xlabel('Words')
    ax.set_ylabel('Weights')

    for label, rect in enumerate(ax.patches):
        height = rect.get_height()
        ax.text(
            rect.get_x() + rect.get_width() / 2, 
            height - 0.035 if height > 0 else height + 0.013,
            round(df['weights'][label],2), 
            ha="center", 
            va="bottom",
            rotation=90, 
            fontsize=8,
            bbox = dict(facecolor = 'whitesmoke', alpha =.8)
        )
    return ax

# Helper function to plot the first image
def plot_1(bar_1, bar_2, tokens_plot_filename):
    plt.rcParams['figure.figsize'] = [20,8]
    plt.rc('font', size = 15)
    
    fig, (ax1, ax2) = plt.subplots(1, 2) 
    fig.suptitle('top 10 most positively and negatively weighted tokens and their weights') 

    ax1 = plot_bar(ax1, bar_1, 'tab:blue', 'tomato', 'PCA: Component 0')
    ax2 = plot_bar(ax2, bar_2, 'skyblue', 'indianred', 'PCA: Component 1')
    plt.savefig(tokens_plot_filename, bbox_inches='tight')
    plt.show()

# Helper function to plot the second image
def plot_2(distribution_plot_filename, X_pca, df):
    plt.rcParams['figure.figsize'] = [8,4]
    plt.rc('font', size = 10)

    sns.scatterplot(x=X_pca[:,0], 
                    y=X_pca[:,1],
                    hue=df['seed_url'].apply(lambda x: re.sub('http://115.146.93.142/samplewiki/', '', x)))
    plt.title("PCA with 2 components")
    plt.xlabel('1st Principal Component')
    plt.ylabel('2nd Principal Component')
    plt.savefig(distribution_plot_filename, bbox_inches='tight')
    plt.show()

# Task 5 - Dimensionality Reduction (3 marks)
def task5(bow_df, tokens_plot_filename, distribution_plot_filename):
    # bow_df is the output of Task 3, for this task you 
    # should generate a bag of words, normalisation of the 
    # data perform PCA decomposition to 2 components, and 
    # then plot all URLs in a way which helps you answer
    # the discussion questions. If you would like to verify 
    # your PCA results against the sample data, you can return
    # the PCA weights - containing the list of most positive
    # weighted words, most negatively weighted words and the 
    # weights in the PCA decomposition for each respective word.
    # Implement Task 5 here

    vectorizer = CountVectorizer()                          # Call the vectorizer method BOW
    bow = vectorizer.fit_transform(bow_df['words'])         # Apply the BOW over the text corpus
    vocabulary = vectorizer.get_feature_names_out()         # Get the corpus names to re-identify them
    df = pd.DataFrame(bow.toarray(), columns=vocabulary)    # Send the Bow sparce patrix to a DF for further treatment
    norm = Normalizer(norm='max')                           # Call the normalizer method
    normalized_data = norm.fit_transform(df)                # Normalize the data by apllying Normalizer
    pca = PCA(n_components=2, random_state = 535)           # Call PCA instance
    result = pca.fit_transform(normalized_data)             # Transform data with pca

    dict_pca = {}
    for val, component in enumerate(pca.components_):       # Function to set dictonary to return

        # Create DF with PCA results
        df = (pd.Series(component, index=vocabulary).       
                sort_values(ascending=False)) 

        # Create DF with top 10 highest and lowest weighted values 
        df = pd.concat([
            df[:10].reset_index(),
            df[-10:].reset_index()],
            axis=1)
        
        # Set colums names
        df.columns = [ 
            'positive', 
            'positive_weights',
            'negative',
            'negative_weights']
        
        # Fill dictionary to return json
        dict_pca[str(val)] = df.iloc[:,[0,2,1,3]].to_dict('list')

    # Save weights of interes of the PCA components to a DF
    bar_1 = get_pca_df(0, pca, vocabulary)  # Component 0
    bar_2 = get_pca_df(1, pca, vocabulary)  # Component 1

    # Plot figure 2
    plot_2(distribution_plot_filename, result, bow_df)

    # Plot figure 1
    plot_1(bar_1, bar_2, tokens_plot_filename)

    return dict_pca

