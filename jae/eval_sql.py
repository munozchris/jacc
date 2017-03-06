# intended to be a util file to be used with a single HTML eval form

import bs4
import re
from eval_sql_util import *
import sqlite3
    
### Usage: ###
# Chris's code call's Jae's code to generate a list of urls for each eval corresponding to a class
# Chris's then creates a soup object for each of the links in that list
# then my code processes each soup object for the information and spits back a dictionary with the information
# for that eval that can be processed into an sql database
# the main scraper that calls this should store the list of evals possibly in a dict

# this code starts based off the assumption that it has the soup object

# driver = webdriver.Chrome("/usr/local/bin/chromedriver")

handler = authenticate()

def make_table():
    conn = sqlite3.connect("eval.db")
    c = conn.cursor()
    t = "DROP TABLE IF EXISTS e_xTA;"
    t2 = "DROP TABLE IF EXISTS e_oTA;"
    t3 = "DROP TABLE IF EXISTS e_bio;"
    t4 = "DROP TABLE IF EXISTS e_lang;"

    c.execute(t)
    c.execute(t2)
    c.execute(t3)
    c.execute(t4)


    e_xTA = "CREATE TABLE e_xTA(\n\
        EvalType TEXT,\n\
        CourseName TEXT,\n\
        CourseNum INT(10000),\n\
        CourseSection TEXT,\n\
        Dept VARCHAR(4),\n\
        Year INT(4),\n\
        Professors TEXT,\n\
        HowFrequentlyAssignmentsDue TEXT,\n\
        InstructorStrengthsComments TEXT,\n\
        InstructorWeaknessesComments TEXT,\n\
        MaxHrs REAL,\n\
        MedHrs REAL,\n\
        MinHrs REAL,\n\
        YesReasonable INT(1000),\n\
        NotReasonable INT(1000),\n\
        NumResponses INT(1000),\n\
        CourseAspectsToChange TEXT,\n\
        DesireToTakeCourse TEXT,\n\
        InstructorEvals TEXT,\n\
        MotivesForTakingClass TEXT)"
    c.execute(e_xTA)

    e_oTA = "CREATE TABLE e_oTA(\n\
        EvalType TEXT,\n\
        CourseName TEXT,\n\
        CourseNum INT(10000),\n\
        CourseSection TEXT,\n\
        Dept VARCHAR(4),\n\
        Year INT(4),\n\
        Professors TEXT,\n\
        MaxHrs REAL,\n\
        MedHrs REAL,\n\
        MinHrs REAL,\n\
        YesReasonable INT(1000),\n\
        NotReasonable INT,(1000),\n\
        NumResponses INT(1000),\n\
        InstructorEvals TEXT,\n\
        AssignmentEvals TEXT,\n\
        OverallEval TEXT)"

    c.execute(e_oTA)

    e_bio = "CREATE TABLE e_bio(\n\
        EvalType TEXT,\n\
        CourseName TEXT,\n\
        CourseNum INT(10000),\n\
        CourseSection TEXT,\n\
        Dept VARCHAR(4),\n\
        Year INT(4),\n\
        Professors TEXT,\n\
        AppropriatenessScore REAL,\n\
        EducativeScore REAL,\n\
        CourseOrganizationScore REAL,\n\
        OverallClassRating REAL,\n\
        PriorExposureScore REAL,\n\
        MaxHrs REAL,\n\
        MedHrs REAL,\n\
        MinHrs REAL,\n\
        NumResponses INT)"
    c.execute(e_bio)

    e_lang = "CREATE TABLE e_lang(\n\
        EvalType TEXT,\n\
        CourseName TEXT,\n\
        CourseNum INT(10000),\n\
        CourseSection TEXT,\n\
        Dept VARCHAR(4),\n\
        Year INT(4),\n\
        Professors TEXT,\n\
        InstructorOrganizationScore REAL,\n\
        ReasonsGoodInstructor TEXT,\n\
        MaxHrs REAL,\n\
        MedHrs REAL,\n\
        MinHrs REAL,\n\
        YesReasonable INT,\n\
        NotReasonable INT,\n\
        NumResponses INT)"
        #RecommendClass#
        #StudiedLanguageBefore#
        #LanguageAspectsStressed#
        #DesireToTakeCourse#
        #ImprovedLanguageSkills#
        #InstructorEvals# 
        #MotivesForTakingClass# 
        #OverallGoodInstructor#
    c.execute(e_lang)

def sql_commit(eval_dict):

    '''
    Given an evaluation dictionary, this code determines which type of evaluation
    it is and then commits it to the corresponding SQL database.
    '''

    conn = sqlite3.connect("eval.db")
    c = conn.cursor()
 
    if eval_dict["EvalType"] == "NOTA":

        sql_query = "INSERT INTO e_xTA (EvalType, CourseName, CourseNum,\
                    CourseSection, Dept, Year, Professors, HowFrequentlyAssignmentsDue,\
                    InstructorStrengthsComments, InstructorWeaknessesComments,\
                    MaxHrs, MedHrs, MinHrs, YesReasonable, NotReasonable, NumResponses,\
                    CourseAspectsToChange, DesireToTakeCourse, InstructorEvals, MotivesForTakingClass)\
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

        data = (eval_dict["EvalType"], eval_dict["CourseName"], eval_dict["CourseNum"],\
                    eval_dict["CourseSection"], eval_dict["Dept"],eval_dict["Year"],\
                    eval_dict["Professors"],eval_dict["HowFrequentlyAssignmentsDue"],\
                    eval_dict["InstructorStrengthsComments"],eval_dict["InstructorWeaknessesComments"],\
                    eval_dict["MaxHrs"],eval_dict["MedHrs"],eval_dict["MinHrs"],\
                    eval_dict["YesReasonable"],eval_dict["NotReasonable"],eval_dict["NumResponses"],\
                    eval_dict["CourseAspectsToChange"], eval_dict["DesireToTakeCourse"],\
                    eval_dict["InstructorEvals"], eval_dict["MotivesForTakingClass"])


        c.execute(sql_query, data)
        conn.commit()


    elif eval_dict["EvalType"] == "YESTA":

        sql_query = "INSERT INTO e_oTA (EvalType, CourseName, CourseNum,\
                    CourseSection, Dept, Year, Professors, MaxHrs, MedHrs, MinHrs,\
                    YesReasonable, NotReasonable, NumResponses, InstructorEvals, AssignmentEvals,\
                    OverallEval) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

        data = (eval_dict["EvalType"], eval_dict["CourseName"], eval_dict["CourseNum"],\
                eval_dict["CourseSection"], eval_dict["Dept"],eval_dict["Year"],\
                eval_dict["Professors"],eval_dict["MaxHrs"],eval_dict["MedHrs"],eval_dict["MinHrs"],\
                eval_dict["YesReasonable"],eval_dict["NotReasonable"],eval_dict["NumResponses"],\
                eval_dict["InstructorEvals"], eval_dict["AssignmentEvals"], eval_dict["OverallEval"])

        c.execute(sql_query, data)
        conn.commit()


    elif eval_dict["EvalType"] == "BIOS":

        sql_query = "INSERT INTO e_bio (EvalType, CourseName, CourseNum,\
                    CourseSection, Dept, Year, Professors, AppropriatenessScore,\
                    EducativeScore, CourseOrganizationScore, OverallClassRating,\
                    PriorExposureScore, MaxHrs, MedHrs, MinHrs, NumResponses)\
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

        data = (eval_dict["EvalType"], eval_dict["CourseName"], eval_dict["CourseNum"],\
                eval_dict["CourseSection"], eval_dict["Dept"],eval_dict["Year"], eval_dict["Professors"],\
                eval_dict["AppropriatenessScore"], eval_dict["EducativeScore"],\
                eval_dict["CourseOrganizationScore"], eval_dict["OverallClassRating"],\
                eval_dict["PriorExposureScore"], eval_dict["MaxHrs"],eval_dict["MedHrs"],\
                eval_dict["MinHrs"], eval_dict["NumResponses"])

        c.execute(sql_query, data)
        conn.commit()

    elif eval_dict["EvalType"] == "LANG":

        sql_query = "INSERT INTO e_lang (EvalType, CourseName, CourseNum,\
                    CourseSection, Dept, Year, Professors, InstructorOrganizationScore,\
                    ReasonsGoodInstructor, MaxHrs, MedHrs, MinHrs,\
                    YesReasonable, NotReasonable, NumResponses)\
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

        data = (eval_dict["EvalType"], eval_dict["CourseName"], eval_dict["CourseNum"],\
                eval_dict["CourseSection"], eval_dict["Dept"],eval_dict["Year"],\
                eval_dict["Professors"], eval_dict["InstructorOrganizationScore"],\
                eval_dict["ReasonsGoodInstructor"], eval_dict["MaxHrs"],eval_dict["MedHrs"],\
                eval_dict["MinHrs"],eval_dict["YesReasonable"],eval_dict["NotReasonable"],\
                eval_dict["NumResponses"])

        c.execute(sql_query, data)
        conn.commit()
    


def get_eval_links(handler, link, threshold_year = 2011):
    soup = get_soup(handler, link)
    table = soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="evalSearchResults")
    
    if not table:
        return None

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
    # handler = authenticate()
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
        
        eval_dict['YesReasonableCourseCount'], eval_dict['NotReasonableCourseCount'] = affirm_reasonable, negative_reasonable

        motives_dict, top_reason, max_count = motives_count, '', 0
        for motive in motives_dict:
            if motives_dict[motive] > max_count:
                top_reason = motive
        eval_dict['TopReasonToTakeClass'] = top_reason



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
        desires_dict = desires_count
        top_sentim, max_count = '', 0
        for val in desires_dict:
            if desires_dict[val] > max_count:
                top_sentim = val
        eval_dict['DesireToTakeCourse'] = top_sentim


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
        instructor_dict = parse_eval_table(soup, 'The Instructor', True)
        instructor_tags = {'Instr_Engaging':'Held my attention and made this course interesting', 'Instr_Organized':'Organized the course clearly',
        'Instr_EffectiveLecturer':'Presented clear lectures', 'Instr_RespondedWellToQuestions':'Responded well to student questions',
        'Instr_AccessibleOutsideClass':'Was available outside of class', 'Instr_HelpfulOfficeHours':'Was helpful during office hours'}
        for tag in instructor_tags:
            eval_dict[tag] = instructor_dict[instructor_tags[tag]]
        
        assignment_dict = parse_eval_table(soup, 'The Assignments', True)
        assignment_tags = {'AppropriateCourseExpectations':'How appropriately were the requirements of the course proportioned to course goals',
        'FairAssignmentGrading':'How fairly were the assignments graded', 'Lecture&DiscussionPreparesStudentsForAssignments':'How helpful were the lectures and discussions in preparing for exams and completing assignments',
        'TimelyAssigmentGrading&Feedback':'How timely and useful was feedback on assignments and exams'}
        for tag in assignment_tags:
            eval_dict[tag] = assignment_dict[assignment_tags[tag]]

        overall_eval_dict = parse_eval_table(soup, 'Overall', True)
        overall_tags = {'AppropriateLevelContent':'The content of this course was presented at an appropriate level',
        'StudentExpectationsMet':'This course met my expectations', 'StudentInsightGain':'This course provided me with new insight and knowledge',
        'StudentSkillsGained':'This course provided me with useful skills'}
        for tag in overall_tags:
            eval_dict[tag] = overall_eval_dict[overall_tags[tag]]


    if Normal_eval:
        instructor_eval_dict = parse_eval_table(soup, 'The Instructor', False)

        instr_labels = {'Instr_EffectiveLecturer':'His/her lectures were clear and understandable', 'Instr_InterestingLecture':'His/her lectures were interesting',
         'Instru_Recommendable':'I would recommend this instructor to others', 'Instr_PositiveTowardStudents':'The instructor exhibited a positive attitude toward student', 
         'Instr_AccessibleOutsideClass':'The instructor was accessible outside of class', 'Instr_Organized':'The instructor was organized'}

        for instr_label in instr_labels:
            eval_dict[instr_label] = instructor_eval_dict[instr_labels[instr_label]]

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
        studied_lang_prior_dict = parse_bar_table(soup, "Have you studied this language before?")
        studied_str = ''
        for key in studied_lang_prior_dict:
            studied_str += key + ': ' + str(studied_lang_prior_dict[key]) + ', '
        eval_dict['StudiedLanguageBefore'] = studied_str[:-2]


        language_aspects_dict = parse_lang_table(soup, 'h3', 
            "Rate to what extent were different aspects of the language stressed.", "gridExtent grid", 6)
        eval_dict['LanguageGrammarEmphasized&Studied'] = language_aspects_dict['Grammar']
        eval_dict['LanguageReadingEmphasized&Studied'] = language_aspects_dict['Reading']
        eval_dict['LanguageSpeakingEmphasized&Studied'] = language_aspects_dict['Speaking']
        eval_dict['LanguageSpellingEmphasized&Studied'] = language_aspects_dict['Spelling']
        eval_dict['LanguageVocabEmphasized&Studied'] = language_aspects_dict['Vocabulary']
        eval_dict['LanguageWritingEmphasized&Studied'] = language_aspects_dict['Writing']


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
        instr_evals = parse_lang_table_wtag(soup, instr_table_tag, "grid1to5 grid", 5)
        instr_evals_tags = {'Instr_FeedbackWasHelpfulRating':'Rate feedback on assignments and exams', 
        'Instr_ConveyedLanguageSubtletiesRating':"Rate instructor's ability to convey the subtleties of the language",
        'Instr_EncouragedLanguageConversationRating':"Rate instructor's ability to encourage class converation in this language",
        'Instr_AccessibleOutsideClass&HelpfulRating':"Rate instructor's availability outside of class and willingness to help"}
        for tag in instr_evals_tags:
            eval_dict[tag] = instr_evals[instr_evals_tags[tag]]

        overall_instr_dict = parse_bar_table(soup, "Overall, would you say you had a good instructor?")
        eval_dict['OverallGoodInstructorYesCount'] = overall_instr_dict['Yes']
        eval_dict['OverallGoodInstructorNoCount'] = overall_instr_dict['No']
        
        good_istr_reasons = [x.text for x in soup.findAll('h3', text="Why?")[1].nextSibling.nextSibling.findAll('li')]
        reasons_str = ''
        for reason in good_istr_reasons:
            reasons_str += reason + ' '
        
        eval_dict['ReasonsGoodInstructor'] = reasons_str[:-1]
        improved_lang_skills_dict = parse_bar_table(soup, "Did taking this course improve your language skills significantly?")
        eval_dict['YesImprovedLanguageSkillsCount'] = improved_lang_skills_dict['Yes']
        eval_dict['NoImprovedLanguageSkillsCount'] = improved_lang_skills_dict['No']

        recommend_dict = parse_bar_table(soup, "Would you recommend this class to another student?")
        eval_dict['WouldRecommendClassCount'] = recommend_dict['Yes']
        eval_dict['WouldNotRecommendClassCount'] = recommend_dict['No']

    return eval_dict



# something like this for how to run it??

def get_info_from_list_of_links(csv_file):

    for url in csv_files:
        all_links = get_eval_links(url)
        for link in all_links:
            eval_info = get_eval_info(link)
            sql_commit(eval_info)


make_table()
get_info_from_list_of_links("../chloe/eval_links.csv")
