'''
eval.db builder 
Buildes the SQLite3 database for all class evaluations
''' 

from eval_sql import *
import csv

print("hey!")
eval_links = []

with open('final_error.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
        eval_links.append(row[0])
    f.close

print("eval links", eval_links)
outfile_name = 'eval_error.csv'
out = csv.writer(open(outfile_name,"w"), delimiter='\n', quoting=csv.QUOTE_ALL)

#csvwriter.writerow([str])
counter, size = 0, len(eval_links)
#make_table()

#eval_links = eval_links[100:500]
#eval_links = eval_links[500:1000]
eval_links = eval_links[:]

for link in eval_links:
    print("link:",link)
    try:
        eval_dict = get_eval_info(url = link)
        #print("Dict")
        #for key, value in eval_dict.items(): 
            #print(key, value)
        print("Processed eval link {} of {}".format(counter, size))
        counter += 1
    except:
        out.writerow([link])
        counter += 1
        continue


    sql_commit(eval_dict)

