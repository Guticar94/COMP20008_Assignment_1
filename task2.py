from bs4 import BeautifulSoup
import requests
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from unicodedata import normalize
import json
from robots import process_robots, check_link_ok

# nltk.download('punkt')
# nltk.download('stopwords')

# Task 2 - Extracting Words from a Page (4 Marks)
def task2(link_to_extract, json_filename):
    # Download the link_to_extract's page, process it 
    # according to the specified steps and output it to
    # a file with the specified name, where the only key
    # is the link_to_extract, and its value is the 
    # list of words produced by the processing.
    # Implement Task 2 here

    # Test robot Rules
    robots_url = 'http://115.146.93.142/robots.txt'                 # Set robots url
    robot_rules = process_robots(requests.get(robots_url).text)     # Get robot rules
    if check_link_ok(robot_rules, link_to_extract):
        try:
            steaming_dict = {}

            page = requests.get(link_to_extract)
            soup = BeautifulSoup(page.content, "html.parser", from_encoding = page.apparent_encoding)


            page_content = soup.find('div', id = 'mw-content-text')         # 1.1 Work in the 'div' element with 'id' = 'mw-content-text'
            [val.decompose() for val in page_content.
                find_all('th', class_ = re.compile('infobox-label'))]       # 1.2 Drop the 'th' elements with 'class' = 'infobox-label'
            [val.decompose() for val in page_content.
                find_all('div', class_ = re.compile('printfooter'))]        # 1.3 Drop the 'div' elements with 'class' = 'printfooter'
            [val.decompose() for val in page_content.
                find_all('div', id = re.compile('toc'))]                    # 1.4 Drop the 'div' elements with 'id' = 'toc'
            [val.decompose() for val in page_content.
                find_all('table', class_ = re.compile('ambox'))]            # 1.5 Drop the 'table' elements with 'class' = 'ambox'
            [val.decompose() for val in page_content.
                find_all('div', class_ = re.compile('asbox'))]              # 1.6 Drop the 'div' elements with 'class' = 'asbox'
            [val.decompose() for val in page_content.
                find_all('span', class_ = re.compile('mw-editsection'))]    # 1.7 Drop the 'span' elements with 'class' = 'mw-editsection'

            text = page_content.getText(separator=u' ')                     # 1.8 Get the page text with space separator

            lowercased = text.lower()                                       # 2.1 casefold: Change text to lower case
            normalized = normalize('NFKD', lowercased)                      # 2.1 Normalization: Normalize text applying NFKD
            no_punct = re.sub(r'([^A-z\s])', ' ', normalized)               # 2.2 Punctuation stripoff: Drop non alphabetical/space characters
            no_punct = re.sub(r'[\s\[\]_]+', ' ', no_punct)                 # 2.3 Spacing characters: Drop repeated spaces and ensure to have only whitespace
            tokens = no_punct.split()                                       # 2.4 Tokenization: Transform text to list of word 
            stop_words = set(stopwords.words('english'))                    # Read English stopwords
            no_stopwords = [w for w in tokens 
                            if not w in stop_words]                         # 2.5 Stopwords: Apply stopwords remover 
            no_stopwords = [w for w in tokens 
                            if not w in stop_words if len(w) >1]            # 2.6 Short tokens: Remove words with less than 2 characters
            porterStemmer = PorterStemmer()                                 # Instantiating the stemmer algorithm
            stemmed = [porterStemmer.stem(w) 
                    for w in no_stopwords]  
            
            steaming_dict[link_to_extract] = stemmed
        except:
            steaming_dict[link_to_extract] = []
    else:   
        steaming_dict[link_to_extract] = []

    # Convert dictionary into JSON and write file
    with open('./Output/'+json_filename +".json", "w") as outfile:
        json.dump(steaming_dict, outfile)