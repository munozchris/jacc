# Course Eval Site Scraper 


import re
import util
import bs4
import queue
import json
import sys
import csv

starting_url = "https://evaluations.uchicago.edu/index.php?EvalSearchType=option-number-search&Department=&CourseDepartment=CMSC&CourseNumber=12200&InstructorLastName=&advancedSearch=SEARCH"

htmlf = "College Course Evaluations | The University of Chicago.html"


f = open(htmlf, 'rb')
def all_URLs(f): 
    '''
    Returns a list of all url links on a single page to follow-up on 

    Inputs: 
        f(str): entire html file in string(?) 
    '''
    f = open(htmlf, 'rb')
    soup = bs4.BeautifulSoup(f.read(), "html5lib")

    tr = soup.tbody.contents
    link_tags = []
    for tags in tr: 
        if tags.td: 
            link_tags.append(tags.td.a["href"])

    return(link_tags)
