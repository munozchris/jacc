# Scraping evals to json files

import csv 
import json

from eval_sql import *
from eval_sql_util import *

filename = 'eval_links1.csv'

eval_links = []
with open(filename, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        eval_links.append(row[0])
    f.close

outfile_name = 'evals_dicts1.json'
fw = open(outfile_name, 'w')

counter, size = 0, len(eval_links)
for link in eval_links:
    eval_dict = get_eval_info(url=link)
    json.dump(eval_dict, fw)
    fw.write('\n')
    print("Processed eval link {} of {}".format(counter, size))
    counter += 1

fw.close()