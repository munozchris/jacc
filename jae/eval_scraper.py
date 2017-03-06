# eval_scraper

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

handler = authenticate()

eval_links = []
counter, size = 2592, len(eval_redirects)

eval_redirects = eval_redirects[2593:]

outfile_name = "eval_links14.csv"
out = csv.writer(open(outfile_name,"w"), delimiter='\n', quoting=csv.QUOTE_ALL)


for link in eval_redirects:
    result = get_eval_links(handler, link)
    
    if not result:
        continue

    out.writerow(result)
    counter += 1
    print('Processed link {} of {}'.format(counter, size))

print("Done.")
