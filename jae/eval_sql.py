# intended to be a util file to be used with a single HTML eval form

import bs4
import re
from eval_sql_util import *
    
    
### Usage: ###
# Chris's code call's Jae's code to generate a list of urls for each eval corresponding to a class
# Chris's then creates a soup object for each of the links in that list
# then my code processes each soup object for the information and spits back a dictionary with the information
# for that eval that can be processed into an sql database
# the main scraper that calls this should store the list of evals possibly in a dict

# this code starts based off the assumption that it has the soup object

# driver = webdriver.Chrome("/usr/local/bin/chromedriver")

#Eval for classes w/o TA: STAT 20000
url1 = 'https://evaluations.uchicago.edu/evaluation.php?id=53790' 
#Eval for classes w/ TA: ARTV 10300
url2 = 'https://evaluations.uchicago.edu/evaluation.php?id=53225' 
#Eval for bio classes: BIOS 10451
url3 = 'https://evaluations.uchicago.edu/evaluationLegacy.php?dept=BIOS&course=10451&section=01&quarter=SPG&year=2011' 
#Eval for language classes: AKKD 10102
url4 = 'https://evaluations.uchicago.edu/evaluation.php?id=41129' 

# handler = authenticate()

# def make_table():
#     conn = sqlite3.connect("eval.db")
#     c = conn.cursor()
#     t = "DROP TABLE IF EXISTS Eval1;"
#     t2 = "DROP TABLE IF EXISTS Eval2;"
#     t3 = "DROP TABLE IF EXISTS Eval3;"
#     t4 = "DROP TABLE IF EXISTS Eval4;"

#     Eval1 = "CREATE TABLE Eval1(\n\
#         EvalType TEXT,\n\
#         CourseId TEXT, \n\
#         CourseName TEXT,\n\
#         CourseSection TEXT,\n\
#         #Professors 
#         Year INT,\n\
#         #Reason for taking course
#         RConcentrationReq INT, \n\
#         RCoreReq INT, \n\
#         RFacultyRec INT, \n\
#         RInstructorRep INT, \n\
#         RConvTime INT, \n\
#         #Motives for taking class
#         MStudentRec INT, \n\
#         MConcentrationElec INT, \n\
#         MConcentrationReq INT, \n\
#         MCoreReq INT, \n\
#         MFacultyRec INT, \n\
#         MInstructorRep INT, \n\
#         MConvTime INT, \n\
#         MTopicInt INT, \n\
#         #Hours spent
#         MinHrs 
#         MedHrs
#         MaxHrs
#         #TIme Commitment Reasonable 
#         TimeYes
#         TimeNo

#         CourseNum TEXT,\n\
#         Title TEXT,\n\
#         EvalLinks TEXT,\n\
#         TotalEnroll INT(10),\n\
#         CurrentTotalEnroll INT(10),\n\
#         StartDate VARCHAR(15),\n\
#         EndDate VARCHAR(15));"

#     Eval2 = "CREATE TABLE SectionInfo(\n\
#             SectionId INT(10000) Primary Key,\n\
#             CourseId INT(10000),\n\
#             Sect TEXT,\n\
#             Professor TEXT,\n\
#             Days1 VARCHAR(100),\n\
#             Days2 VARCHAR(100),\n\
#             StartTime1 INT,\n\
#             StartTime2 INT,\n\
#             EndTime1 INT,\n\
#             EndTime2 INT,\n\
#             SectionEnroll INT(10),\n\
#             CurrentSectionEnroll INT(10));"
    
    
#     Eval3 = "CREATE TABLE ProfTable(\n\
#                 Professor VARCHAR(1000),\n\
#                 CourseId INT(10000),\n\
#                 SectionId INT(1000));"


#     Eval4= "CREATE TABLE Description(\n\
#                         CourseId INT(10000),\n\
#                         Description TEXT);"


#     c.execute(t)
#     c.execute(t2)
#     c.execute(t3)
#     c.execute(t4)
#     c.execute(CourseInfo)
#     c.execute(SectionInfo)
#     c.execute(ProfTable)
#     c.execute(DescTable)
#     c.close()    
    
    
    
def get_eval_links(link, threshold_year = 2011):
    get_soup(handler, link)
    table = soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="evalSearchResults")
    rows = table.findAll(lambda tag: tag.name=='tr')

    # note: it's find and findAll 
    links = []
    for row in rows[1:]:
        quarter = row.contents[7].text
        year = int(re.search(r'\d{4}', quarter).group())
        year = int(re.search(r'\d{4}', quarter).group())
        if year > threshold_year:
            links.append(row.td.a['href'])

    abs_urls = []
    for link in links:
        abs_link = convert_if_relative_url(url2, link)
        abs_urls.append(abs_link)

    return abs_urls
    


def get_eval_info(url = None, soup = None):
    handler = authenticate()
    soup = get_soup(handler, url)

    BIOS_eval = False
    Language_eval = False
    TA_eval = False
    Normal_eval = False
    
    eval_dict = {}
    keys = ['CourseId', 'CourseName', 'SectionId']

    course_full = soup.find(class_="eval-page-title").text
    course_code = re.findall(r'([A-Z\s0-9]*:)(.*)', course_full)[0][0][:-1]
    parts = re.findall(r'([A-Z]{4})(.*)', course_code)
    dept, class_num = parts[0][0], parts[0][1][1:]
    course_name = re.findall(r'([A-Z\s0-9]*:)(.*)', course_full)[0][1][1:]
    course_section = soup.find(class_="section-title").text
    year = int(re.search(r'\d{4}', course_section).group())

    # splits multiple instructors
    instr_list = str(soup.findAll('strong', text='Instructor(s):')[0].nextSibling)[1:].split('; ')
    formatted_instrs = []
    for full_name in instr_list:
        name_parts = full_name.split(', ')
        formatted_instrs.append(name_parts[1] + ' ' + name_parts[0])
    instructors_str = ''
    for name in formatted_instrs:
        name += ', '
        instructors_str += name
    instructors_str = instructors_str[:-2]

    num_responses = int(str(soup.findAll('strong', text='Number of Responses:')[0].nextSibling).strip())

    eval_dict['Dept'], eval_dict['CourseNum'] = dept, int(class_num)
    eval_dict['CourseName'], eval_dict['Professors'] = course_name, instructors_str
    eval_dict['NumResponses'], eval_dict['CourseSection'], eval_dict['Year'] = num_responses, course_section, year

    max_hr, med_hr, min_hr = 0, 0, 0

    # Bio-type eval
    bio_time = soup.find('th', text='How many hours did you spend each week preparing for this class (including labs)? (0-9 + hours scale)')
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


    if not BIOS_eval:
        affirm_reasonable, negative_reasonable = 'null', 'null'
        motives_count = {}
        desires_count = {}
        affirm_responses = soup.find('h3', text='Were the time demands of this course reasonable?').nextSibling.nextSibling.contents[3].next_element.contents[5].text
        affirm_num = int(re.search(r'\d+', affirm_responses).group())
        negative_responses = soup.find('h3', text='Were the time demands of this course reasonable?').nextSibling.nextSibling.contents[3].find_all('td')[3].text
        negative_num = int(re.search(r'\d+', negative_responses).group())
        affirm_reasonable, negative_reasonable = affirm_num, negative_num

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
        
        eval_dict['YesReasonable'], eval_dict['NotReasonable'] = affirm_reasonable, negative_reasonable

        eval_dict['MotivesForTakingClass'] = motives_count


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
        options_list = soup.find('h3', text='In summary, I had a strong desire to take this course').nextSibling.nextSibling.find_all('th')
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
            desires_count[desires_strs[i]] = counts_list[i]
    elif TA_eval:
        desires_tds = soup.find('h3', text='In summary, I had a strong desire to take this course').nextSibling.nextSibling.find_all('td', attrs = {'class':'count-totals'})
        desires_counts = []
        for td in desires_tds:
            count = int(re.search(r'\d+', td.text).group())
            desires_counts.append(count)
        for i in range(len(desires_strs)):
            desires_count[desires_strs[i]] = counts_list[i]

    if not BIOS_eval:
        eval_dict['DesireToTakeCourse'] = desires_count


    if BIOS_eval:
        eval_dict['EvalType'] = 'BIOS'
    elif Language_eval:
        eval_dict['EvalType'] = 'LANG'
    elif TA_eval:
        eval_dict['EvalType'] = 'YESTA'
    else:
        eval_dict['EvalType'] = 'NOTA'


    if BIOS_eval:
        organized_text = soup.find('td', text='The course was well organized').nextSibling.nextSibling.text
        organized_score = float(re.search(r'\d\.\d', organized_text).group())
        eval_dict['CourseOrganizationScore'] = organized_score

        skills_text = soup.find('td', text='The course provided me with useful knowledge, skills, or insights.').nextSibling.nextSibling.text
        skills_score = float(re.search(r'\d\.\d', skills_text).group())
        eval_dict['EducativeScore'] = skills_score

        appropr_text = soup.find('td', text='The content material was presented at an appropriate level.').nextSibling.nextSibling.text
        appropr_score = float(re.search(r'\d\.\d', appropr_text).group())
        eval_dict['AppropriatenessScore'] = appropr_score

        overall_text = soup.find('td', text='Overall this was an outstanding course.').nextSibling.nextSibling.text
        overall_score = float(re.search(r'\d\.\d', overall_text).group())
        eval_dict['OverallClassRating'] = overall_score

        prior_text = soup.find('th', text='How much prior exposure did you previously have to the topics covered in this course? (1 = not at all, 5 = a great deal)').nextSibling.nextSibling.text
        prior_score = float(re.search(r'\d\.\d', prior_text).group())
        eval_dict['PriorExposureScore'] = prior_score


    if TA_eval:
        eval_dict['InstructorEvals'] = parse_eval_table(soup, 'The Instructor', True)
        eval_dict['AssignmentsEvals'] = parse_eval_table(soup, 'The Assignments', True)
        eval_dict['OverallEval'] = parse_eval_table(soup, 'Overall', True)


    if Normal_eval:
        eval_dict['InstructorEvals'] = parse_eval_table(soup, 'The Instructor', False)
        eval_dict['InstructorStrengthsComments'] = get_comments_list(soup, 'h3', 
            "What were the instructor's strong points?")
        eval_dict['InstructorWeaknessesComments'] = get_comments_list(soup, 'h3', 
            "What were the instructor's weak points?")
        eval_dict['CourseAspectsToRetain'] = get_comments_list(soup, 'h3', 
            "What aspects of the course should be changed?")
        eval_dict['CourseAspectsToChange'] = get_comments_list(soup, 'h3', 
            "What aspects of the course should be changed?")

        # Assigments
        row_text = [x.text for x in soup.find('h3', text="How often were homework assignments due?").nextSibling.nextSibling.findAll('th')]
        col_counts = count_tags = [int(re.search(r'\d+', x.text).group()) for x in soup.find('h3', 
            text="How often were homework assignments due?").nextSibling.nextSibling.findAll('td', {'class':'count-totals'})]
        index_min = min(range(len(col_counts)), key=col_counts.__getitem__)
        eval_dict['HowFrequentlyAssignmentsDue'] = row_text[index_min]

    if Language_eval:
        eval_dict['StudiedLanguageBefore'] = parse_bar_table(soup, "Have you studied this language before?")
        eval_dict['LanguageAspectsStressed'] = parse_lang_table(soup, 'h3', 
            "Rate to what extent were different aspects of the language stressed.", "gridExtent grid", 6)
        
        org_text = parse_lang_table(soup, 'h2', "The Instructor", "grid1to5 grid", 5)
        nums = re.findall(r'\d+', org_text)
        if len(nums) > 1:
            score = 0
            for num in nums:
                num = int(num)
                score += num
            score = score/len(nums)
        else:
            score = int(nums[0])
        eval_dict['InstructorOrganizationScore'] = score

        instr_table_tag = soup.findAll('table', {'class':'table-evals'})[22]
        eval_dict['InstructorEvals'] = parse_lang_table_wtag(soup, instr_table_tag, "grid1to5 grid", 5)

        eval_dict['OverallGoodInstructor'] = parse_bar_table(soup, "Overall, would you say you had a good instructor?")
        
        good_istr_reasons = [x.text for x in soup.findAll('h3', text="Why?")[1].nextSibling.nextSibling.findAll('li')]
        reasons_str = ''
        for reason in good_istr_reasons:
            reasons_str += reason + ' '
        
        eval_dict['ReasonsGoodInstructor'] = reasons_str[:-1]
        eval_dict['ImprovedLanguageSkills'] = parse_bar_table(soup, "Did taking this course improve your language skills significantly?")
        eval_dict['RecommendClass'] = parse_bar_table(soup, "Would you recommend this class to another student?")

    return eval_dict





