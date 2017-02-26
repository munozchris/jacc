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

# STAT 20000 eval sample
url1 = 'https://evaluations.uchicago.edu/evaluation.php?id=53790'
url2 = 'https://evaluations.uchicago.edu/evaluationLegacy.php?dept=BIOS&course=10451&section=01&quarter=SPG&year=2011'
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

eval_dict['CourseId'], eval_dict['CourseName'] = course_code, course_name


quit()




