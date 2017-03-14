CS 122-FinalProject: EvaluationsCode Directory 

This directory contains necessary code needed to scrape:
1) Evaluation links from my.classes course offerings
2) Evaluation forms between year 2011-2016 on each class offering 

1. gateway_links_processor.py
Automator script that gathers all absolute links to class evaluations
from post-2011 and writes them out to eval_links.csv

2. eval_links.csv 
Contains all evaluation form links that should be processed and
put into the database

3. eval_sql.py
1) Builds a SQL database to contain evaluaion form information
2) Processes eval_links.csv file by scraping the content of each 
evaluation form

4. eval_sql_uitl.py
Some helper functions for eval_sql.py

5. make_plots.py
Functions that generates analysis plots based on information from evaluations



