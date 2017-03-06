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
counter, size = 2291, len(eval_redirects)

eval_redirects = eval_redirects[2292:]

for link in eval_redirects:
    result = get_eval_links(handler, link)
    if not result:
        continue
    eval_links += result
    counter += 1
    print('Processed link {} of {}'.format(counter, size))

print("Exited for-loop.")
out = csv.writer(open("eval_links7.csv","w"), delimiter='\n',quoting=csv.QUOTE_ALL)
out.writerow(eval_links)
