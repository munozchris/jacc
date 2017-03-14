# gateway_links_processor

'''
### USAGE ###
Automator script that gathers all absolute links to class evaluations
from post-2011 and writes them out to a csv file 
called "eval_links_corrected"

First combines the gateway links gathered from class information
scraping that were stored as two .csv files and combines
them into a list of urls to process 

if the class does not have evaluations this script moves on 
to the next gateway link

links are written out onto the outfile as each gateway link 
is processed

Also prints status to terminal
'''

import csv
from eval_sql import *
from eval_sql_util import *

eval_redirects = []

with open('../chloe/eval_links.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        eval_redirects.append(row[0])
    f.close


with open('../chloe/final_eval_links.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        eval_redirects.append(row[0])
    f.close

# handler = authenticate()

eval_links = []
# counter, size = 2594, len(eval_redirects)
# reset counter below:
counter, size = 0, len(eval_redirects)

# eval_redirects = eval_redirects[2595:]

outfile_name = "eval_links.csv"
out = csv.writer(open(outfile_name,"w"), delimiter='\n', quoting=csv.QUOTE_ALL)


for link in eval_redirects:
    result = get_eval_links(link)
    
    counter += 1
    print('Processed link {} of {}'.format(counter, size))

    if not result:
        continue
        
    out.writerow(result)


print("Done.")

# test should produce 5 links.
