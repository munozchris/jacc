# eval_db_builder.py

'''
### USAGE ### 
Buildes the SQLite3 database for all class evaluations
Given a csv file of all absolute links to class evaluations

If any error comes up with extracting data from an eval_link, this script
writes the problematic url to an outfile called "eval_error_log.csv"
and moves on to the next eval_link

eval_links in the error log need to be proceed on a case-by-case basis

Prints out status to terminal
''' 

from eval_sql import *
import csv

eval_links = []

eval_links_filename = "eval_links.csv"
with open(eval_links_filename, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
        eval_links.append(row[0])
    f.close


outfile_name = 'eval_error_log.csv'
out = csv.writer(open(outfile_name,"w"), delimiter='\n', quoting=csv.QUOTE_ALL)

# to use with multiple strings to write out in a list: csvwriter.writerow([str])
counter, size = 0, len(eval_links)

# if this script freezes up/stops unexpectedly, begin processing where you left off
# eval_links = eval_links[100:500]
# eval_links = eval_links[500:1000]

for link in eval_links:
    # print("Now processing link: ", link)
    try:
        eval_dict = get_eval_info(url = link)
        print("Processed eval link {} of {}".format(counter, size))
        counter += 1
    except:
        out.writerow([link])
        counter += 1
        continue

    sql_commit(eval_dict)

print("Done.")
