# intended to be a util file to be used with a single HTML eval form

import bs4
import re
from util import *

### Usage: ###
# Chris's code call's Jae's code to generate a list of urls for each eval corresponding to a class
# Chris's then creates a soup object for each of the links in that list
# then my code processes each soup object for the information and spits back a dictionary with the information
# for that eval that can be processed into an sql database
# the main scraper that calls this should store the list of evals possibly in a dict

# this code starts based off the assumption that it has the soup object
BIOS_eval = False
Language_eval = False
TA_eval = False
Normal_eval = False

# STAT 20000 eval sample
url1 = 'https://evaluations.uchicago.edu/evaluation.php?id=53790' # eval for class w/o TA; STAT 20000
url2 = 'https://evaluations.uchicago.edu/evaluationLegacy.php?dept=BIOS&course=10451&section=01&quarter=SPG&year=2011' # eval for bio class; BIOS 10451
url3 = 'https://evaluations.uchicago.edu/evaluation.php?id=41129' # eval for language class; AKKD 10102
url4 = 'https://evaluations.uchicago.edu/evaluation.php?id=53225' # eval for class w/ TA's; ARTV 10300
soup = get_soup(url1)

# def get_eval_info(soup):
eval_dict = {}
keys = ['CourseId', 'CourseName', 'SectionId']

course_full = soup.find(class_="eval-page-title").text
course_code = re.findall(r'([A-Z\s0-9]*:)(.*)', course_full)[0][0][:-1]
course_name = re.findall(r'([A-Z\s0-9]*:)(.*)', course_full)[0][1][1:]
course_section = soup.find(class_="section-title").text

# splits multiple instructors
instr_list = str(soup.findAll('strong', text='Instructor(s):')[0].nextSibling)[1:].split(';')
formatted_instrs = []
for full_name in instr_list:
    name_parts = full_name.split(', ')
    formatted_instrs.append(name_parts[1] + ' ' + name_parts[0])

num_responses = int(str(soup.findAll('strong', text='Number of Responses:')[0].nextSibling).strip())

eval_dict['CourseId'], eval_dict['CourseName'], eval_dict['Professors'] = course_code, course_name, formatted_instrs
eval_dict['NumResponses'] = num_responses

max_hr, med_hr, min_hr = 0, 0, 0

# Bio-type eval
bio_time = soup.find('th', text='How many hours did you spend each week preparing for this class (including labs)? (0-9 + hours scale)'):
if bio_time is not None:
    bio_time = bio_time.nextSibling.nextSibling
    BIOS_eval = True
    num_str = bio_time.contents[2]
    num_list = re.findall(r'\d+\.\d*', num_str)
    mean, stdv = float(num_list[0]), float(num_list[1])
    min_hr, med_hr, max_hr = mean - stdv, mean, mean + stdv

# if language class
language_time = soup.find('h3', text="How many hours did you spend?")
if language_time is not None:
    Language_eval = True
    language_time = language_time.nextSibling.nextSibling.contents[3]
    low_text = language_time.contents[0].text
    avg_text = language_time.contents[2].text
    high_text = language_time.contents[4].text
    min_hr = float(re.search(r'\d+\.*\d*', low_text).group())
    med_hr = float(re.search(r'\d+\.*\d*', avg_text).group())
    max_hr = float(re.search(r'\d+\.*\d*', high_text).group())

# else standard TA/no TA-type eval
normal_time = soup.find('h3', text='How many hours per week did you spend on this course?')
if normal_time is not None:
    normal_time = normal_time.nextSibling.nextSibling.contents[3]
    low_text = normal_time.contents[0].text
    avg_text = normal_time.contents[2].text
    high_text = normal_time.contents[4].text
    min_hr = float(re.search(r'\d+\.*\d*', low_text).group())
    med_hr = float(re.search(r'\d+\.*\d*', avg_text).group())
    max_hr = float(re.search(r'\d+\.*\d*', high_text).group())

eval_dict['MinHrs'], eval_dict['MedHrs'], eval_dict['MaxHrs'] = min_hr, med_hr, max_hr

affirm_reasonable = 'null', negative_resonable = 'null'
motives_count = {}
desires_count = {}

if not BIOS_eval:
    affirm_responses = soup.find('h3', text='Were the time demands of this course reasonable?').nextSibling.nextSibling.contents[3].next_element.contents[5].text
    affirm_num = int(re.search(r'\d+', affirm_responses).group())
    negative_responses = soup.find('h3', text='Were the time demands of this course reasonable?').nextSibling.nextSibling.contents[3].find_all('td')[3].text
    negative_num = int(re.search(r'\d+', negative_responses).group())
    total
    affirm_reasonable, negative_resonable = affirm_num, negative_num

    motives_th_list = soup.find('h3', text='Why did you take this course?').nextSibling.nextSibling.find_all('th')
    motives_strs = []
    for th in motives_th_list:
        motives_strs.append(th.text)
    td_counts = soup.find('h3', text='Why did you take this course?').nextSibling.nextSibling.find_all('td', attrs = {'class':'count-totals'})
    counts_list = []
    for td in td_counts:
        count = int(re.search(r'\d+', td.text).group())
        counts_list.append(count)
    for i in range(len(motives_strs)):
        motives_count[motives_strs[i]] = counts_list[i]
    eval_dict['']


desire_tag = soup.find('h3', text='In summary, I had a strong desire to take this course.')
if not Language_eval and desire_tag is not None:
    Normal_eval = True
elif not BIOS_eval and desire_tag is None:
    TA_eval = True

if Normal_eval or Language_eval:
    options_list = desire_tag.nextSibling.nextSibling.find_all('th')
    desires_strs = []
    for option in options_list:
        desires_strs.append(option.text)
elif TA_eval:
    options_list = soup.find('h3', text='In summary, I had a strong desire to take this course').find_all('th')
    desires_strs = []
    for option in options_list:
        desires_strs.append(option.text)    
if Normal_eval or Language_eval:
    desires_tds = soup.find('h3', text='In summary, I had a strong desire to take this course.').nextSibling.nextSibling.find_all('td', attrs = {'class':'count-totals'})
    desires_counts = []
    for td in desires_tds:
        count = int(re.search(r'\d+', td.text).group())
        desires_counts.append(count)
    for i in range(len(desires_strs)):
        desires_count[motives_strs[i]] = counts_list[i]
elif TA_eval:
    desires_tds = soup.find('h3', text='In summary, I had a strong desire to take this course').nextSibling.nextSibling.find_all('td', attrs = {'class':'count-totals'})
    desires_counts = []
    for td in desires_tds:
        count = int(re.search(r'\d+', td.text).group())
        desires_counts.append(count)
    for i in range(len(desires_strs)):
        desires_count[motives_strs[i]] = counts_list[i]

if BIOS_eval:
    eval_dict['EvalType'] = 'BIOS'
elif Language_eval:
    eval_dict['EvalType'] = 'LANG'
elif TA_eval:
    eval_dict['EvalType'] = 'YESTA'
else:
    eval_dict['EvalType'] = 'NOTA'

quit()




