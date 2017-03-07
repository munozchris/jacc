# eval_db builder

from eval_sql import *
import csv

eval_links = []

with open('eval_links.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        eval_links.append(row[0])
    f.close

outfile_name = "eval_error_log.csv"
out = csv.writer(open(outfile_name,"w"), delimiter='\n', quoting=csv.QUOTE_ALL)

#csvwriter.writerow([str])
counter, size = 298, len(eval_links)
make_table()

eval_links = eval_links[299:]

for link in eval_links:
    try:
        eval_dict = get_eval_info(url = link)
        counter += 1
        print("Processed eval link {} of {}".format(counter, size))
    except:
        out.writerow([link])
        continue

    sql_commit(eval_dict)

