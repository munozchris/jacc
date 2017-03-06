# eval_scraper

import csv
from eval_sql import *
from eval_sql_util import *

eval_redirects = []

# with open('../chloe/eval_links.csv', 'r') as f:
with open('eval_redirects_almostdone.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        eval_redirects.append(row[0])
    f.close


# with open('../chloe/final_eval_links.csv', 'r') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         eval_redirects.append(row[0])
#     f.close

# handler = authenticate()

# eval_links = []
# counter, size = 2594, len(eval_redirects)
# reset counter below:
counter, size = 0, len(eval_redirects)

# eval_redirects = eval_redirects[2595:]

# outfile_name = "eval_redirects_almostdone.csv"
# out = csv.writer(open(outfile_name,"w"), delimiter='\n', quoting=csv.QUOTE_ALL)
# out.writerow(eval_redirects)


outfile_name = "eval_links8.csv"
out = csv.writer(open(outfile_name,"w"), delimiter='\n', quoting=csv.QUOTE_ALL)


for link in eval_redirects:
    result = get_eval_links(handler, link)
    
    if not result:
        print("No links!")
        continue

    out.writerow(result)
    counter += 1
    print('Processed link {} of {}'.format(counter, size))

print("Done.")
