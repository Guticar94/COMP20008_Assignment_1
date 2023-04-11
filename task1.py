""" 
COMP20008 Semester 1
Assignment 1 Task 1
"""

from bs4 import BeautifulSoup
import requests
import re
from robots import process_robots, check_link_ok
from urllib.parse import urljoin
import json

# A simple page limit used to catch procedural errors.
SAFE_PAGE_LIMIT = 1000

# Helper function to crawl specified link
def crawl_seed(seed_url, robot_rules):         # Function to get the url's list
    page = requests.get(seed_url)       # Fetch page
    soup = BeautifulSoup(page.text, 
            'html.parser')              # Seed URL text
    links = soup.findAll('a')           # Find new links to visit 

    # Get links to visit according rules
    to_visit = [urljoin(seed_url, l['href']) 
        for l in links 
        if "href" in l.attrs                              # 1. 'a' elements with href atributes
        if check_link_ok(robot_rules, l['href'])]         # 2. Follow robot rules

    to_visit = list(set([re.sub('#.*', '', i)             # 3. Drop repeated pages
        for i in to_visit 
        if re.match(r'^http://115.146.93.142.*$', i)]))   # 4. Get self domain url's
    return  to_visit

# Task 1 - Get All Links (3 marks)
def task1(starting_links, json_filename):
# Crawl each url in the starting_link list, and output
# the links you find to a JSON file, with each starting
# link as the key and the list of crawled links for the
# value.
# Implement Task 1 here

    base = 'http://115.146.93.142'                                          # Specify base path for the excercise
    robots_item = '/robots.txt'                                             # Specify the location of robots.txt
    robots_url = base + robots_item                                         # Set robots url
    robot_rules = process_robots(requests.get(robots_url).text)             # Get robot rules
    crawled_links = {}                                                      # Set dictionary to gather results to Json format
    page_counter = 1                                                        # Set counter to break loop if reaches limit

    # Iterate over starting_links url's
    for seed_link in starting_links:
        
        visited = []                                    # Inicialise dictionary to save crawled links 
        link_to_crawl = seed_link                       # Save link to crawl
        to_visit = crawl_seed(link_to_crawl, robot_rules)            # Get list of links to visit from current seed link

        while(to_visit):                                # Iterate while there are remaining links to visit

            # Break loop if reaches limit of pages crawled
            if(page_counter == SAFE_PAGE_LIMIT): 
                break  
            next_link = to_visit.pop(0)                 # Select link and drop from the list of links to visit 

            if next_link not in visited:                # If the selected link has not been visited, crawl it
                visited.append(next_link)               # Append to list of links to visit
                page_counter += 1                        # Increment counter
                new_to_visit = crawl_seed(next_link, robot_rules)    # Get list of links to visit from current seed link 

                # Append links to list of links to visit if the link has not been visited and is not in the links to visit list
                [to_visit.append(new_link) 
                        for new_link in new_to_visit 
                            if ((not new_link in visited) 
                                and (not new_link in to_visit))]
        
        # Save links to dictionary with parenth seed link
        crawled_links[link_to_crawl] = sorted(visited)                   
    # Convert dictionary into JSON and write file
    with open('./Output/'+json_filename+'.json', "w") as outfile:
        json.dump(crawled_links, outfile)