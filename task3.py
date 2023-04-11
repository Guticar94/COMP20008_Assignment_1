""" 
COMP20008 Semester 1
Assignment 1 Task 3
"""

import json
import pandas as pd
import task2


# Task 3 - Producing a Bag Of Words for All Pages (2 Marks)
def task3(link_dictionary, csv_filename):
    # link_dictionary is the output of Task 1, it is a dictionary
    # where each key is the starting link which was used as the 
    # seed URL, the list of strings in each value are the links 
    # crawled by the system. The output should be a csv which
    # has the link_url, the words produced by the processing and
    # the seed_url it was crawled from, this should be output to
    # the file with the name csv_filename, and should have no extra
    # numeric index.
    # Implement Task 3 here

    # Empty dataframe to demonstrate output data format.
    dataframe = pd.DataFrame(columns=['link_url', 'words', 'seed_url'])

    for seed in link_dictionary.keys():     # Iterate over seed urls
        for url in link_dictionary[seed]:   # Iterate over link urls

            task2.task2(url, 'json_filename_2')             # Write to Json the List of words

            with open('./Output/json_filename_2.json', 'r') as rf:
                word_list = [' '.join(val)                  # Get the list og words from json
                    for val in json.load(rf).values()][0]
                
            to_append = {           # Save values to a dict
                'link_url': [url],
                'words': [word_list], 
                'seed_url' : [seed]}
            
            dataframe = pd.concat(  # Apend dict to dataframe
                [pd.DataFrame(to_append),
                 dataframe.loc[:]]).reset_index(drop=True)
    
    
    dataframe = (dataframe.         # Order values ascending
                 sort_values(['link_url','seed_url']).
                 reset_index(drop=True))   
    
    dataframe.to_csv('./Output/'+csv_filename+'.csv', index= False)  # Save DataFrame to csv