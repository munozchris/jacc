import csv

eval_links = []

with open('eval_links.csv', 'r') as f:
    reader = csv.reader(f, delimiter=' ')
    for row in reader:
        eval_links.append(row)
    f.close

eval_links = eval_links[0]


out = csv.writer(open("eval_links1.csv","w"), delimiter='\n',quoting=csv.QUOTE_ALL)
out.writerow(eval_links)