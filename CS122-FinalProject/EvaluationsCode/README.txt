CS 122-FinalProject: EvaluationsCode Directory 

This directory contains necessary code needed to scrape:
1) Evaluation links from my.classes course offerings
2) Evaluation forms between year 2011-2016 on each class offering 

1. gateway_links_processor.py
Automator script that gathers all absolute links to class evaluations
from post-2011 and writes them out to eval_links.csv from gateway links

2. gateway_links1.csv and gateway_links2.csv
Contains the list of all gateway_links from course scraping to be
processed to find absolute evaluation form links

3. eval_links.csv 
Contains all evaluation form links that should be processed and
put into the database

4. eval_sql.py
1) Builds a SQL database to contain evaluaion form information
2) Processes eval_links.csv file by scraping the content of each 
evaluation form

5. eval_sql_util.py
Some helper functions for eval_sql.py

6. make_plots.py
Functions that generates analysis plots based on information from evaluations

7. eval_error_log.py, eval_error_log2.py, eval_error_log3.py
List of absolute urls to evaluation forms that couldn't be automatically 
processed and needed to be manually entered into the database/absolute
links to evaluation forms that required us to modify our evaluation scraping
code

8. README.txt
This file

