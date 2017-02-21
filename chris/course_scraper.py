from selenium import webdriver  
from selenium.common.exceptions import NoSuchElementException  
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from time import sleep
#from login_save import get_auth_driver

import bs4  
import re
import csv
import sqlite3

COUNTER = 0

def make_table():
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    t = "DROP TABLE IF EXISTS CourseInfo;"
    t2 = "DROP TABLE IF EXISTS ProfTable;"
    t3 = "DROP TABLE IF EXISTS MeetingPatterns"

    CourseInfo = "CREATE TABLE CourseInfo(\n\
        CourseId INT(10000) Primary Key,\n\
        Dept VARCHAR(4),\n\
        CourseNum TEXT,\n\
        Sect TEXT,\n\
        Title TEXT,\n\
        Desc TEXT,\n\
        Days VARCHAR(100),\n\
        StartTime INT,\n\
        EndTime INT,\n\
        SectionEnroll VARCHAR(10),\n\
        TotalEnroll VARCHAR(10),\n\
        StartDate VARCHAR(15),\n\
        EndDate VARCHAR(15));"
    
    ProfTable = "CREATE TABLE ProfTable(\n\
                CourseId INT(10000),\n\
                Professor VARCHAR(1000),\n\
                Dept VARCHAR(4),\n\
                CourseNum TEXT,\n\
                Sect TEXT);"

    MeetingPatterns = "CREATE TABLE MeetingPatterns(\n\
                        CourseId INT(10000),\n\
                        Days VARCHAR(100),\n\
                        Times INT(2400),\n\
                        StartTime TEXT,\n\
                        EndTime TEXT,\n\
                        StartDate VARCHAR(15),\n\
                        EndDate VARCHAR(15));"

    c.execute(t)
    c.execute(t2)
    c.execute(t3)
    c.execute(CourseInfo)
    c.execute(ProfTable)
    c.execute(MeetingPatterns)
    c.close()


def get_course_info(soup, index):
    '''
    Given the page source in beautiful Soup format,
    returns a dictionary of all the info from the page
    '''


    class_info_dict = {"Professors": [], "Days": []}

    # Get course title
    course_title = soup.find(class_="ps_box-value", id="UC_CLSRCH_WRK_UC_CLASS_TITLE$"+str(index))
    class_info_dict["Title"] = course_title.text

    # Get department, course number, section number, and course ID
    intermediate = soup.find_all(class_=["label label-success", "label label-default"])
    #if intermediate is None:
        #intermediate = soup.find_all(class_="label label-default")
    information = intermediate[index].parent.text
    dept = re.search("[A-Z]{4}", information)
    course_nums = re.findall("[0-9]{5}", information)
    course_num = course_nums[0]
    global COUNTER
    COUNTER += 1
    course_id = COUNTER
    section_num = re.search("[0-9] ", information)

    class_info_dict["CourseNum"] = course_num
    class_info_dict["Dept"] = dept.group()
    class_info_dict["Sect"] = section_num.group().strip()
    class_info_dict["CourseId"] = course_id

            
    #if it exists
    total_enrollment = soup.find(class_="ps_box-value", id="UC_CLSRCH_WRK_DESCR2$"+str(index))
    text = total_enrollment.text
    numbers = text[18:]
    class_info_dict["TotalEnroll"] = numbers
     
    # if it exists
    section_enrollment = soup.find(class_="ps_box-value", id="UC_CLSRCH_WRK_DESCR1$"+str(index))
    text = section_enrollment.text
    numbers = text[20:]
    class_info_dict["SectionEnroll"] = numbers

    prof = soup.find(class_="ps_box-value", id="MTG$0")
    text = prof.text
    all_profs = re.findall("[A-Z][A-Za-z\s]+", text)
    for professor in all_profs:
        class_info_dict["Professors"].append(professor)


    times_and_day = soup.find(class_="ps_box-value", id="MTG_SCHED$0") # Messed up in Aramaic (got 12, not 10:30)
    text = times_and_day.text

    days = re.findall("[A-Z][a-z]+", text)
    for day in days:
        class_info_dict["Days"].append(day)

    times = re.findall("[0-9][0-9]:[0-9][0-9] [A-Z][A-Z]", text)

    if len(times) == 2:

        start_time = times[0]
        hour = start_time[:2]
        minute = start_time[3:5]
        if start_time[6:] == "PM" and hour != "12":
            hour = str(int(hour)+12)
        start_time = int(hour+minute)
        class_info_dict["StartTime"] = start_time

        end_time = times[1]
        hour = end_time[:2]
        minute = end_time[3:5]
        if end_time[6:] == "PM":
            hour = str(int(hour)+12)
        end_time = int(hour+minute)
        class_info_dict["EndTime"] = end_time

    timeframe = soup.find(class_="ps_box-value", id="MTG_DATE$0")
    text = timeframe.text
    start_date = text[:10]
    end_date = text[13:]
    class_info_dict["StartDate"] = start_date
    class_info_dict["EndDate"] = end_date
    
    return class_info_dict


def create_list():
    '''
    Makes a list of dictionaries for every class, going through all departments
    and scraping the html
    '''

    url = 'https://coursesearch.uchicago.edu/psc/prdguest/EMPLOYEE/HRMS/c/UC_STUDENT_RECORDS_FL.UC_CLASS_SEARCH_FL.GBL'
    # browser = webdriver.Chrome()  
    # browser.get(url)
    url2 = 'https://evaluations.uchicago.edu/index.php?EvalSearchType=option-number-search&Department=&CourseDepartment=AKKD&CourseNumber=10102&InstructorLastName=&advancedSearch=SEARCH'
    #browser = get_auth_driver(url2)
    
    browser = webdriver.Chrome()  
    browser.get(url)


    el = browser.find_element_by_id('win0divUC_CLSRCH_WRK2_SUBJECTctrl') # find the dropdown menu
    submit = browser.find_element_by_id("UC_CLSRCH_WRK2_SEARCH_BTN") # find the submit button
    wait = WebDriverWait(browser, 10)

    select = Select(browser.find_element_by_id("UC_CLSRCH_WRK2_STRM"))
    select.select_by_value('2174')
    #conn = sqlite3.connect(sql_filename)
    #c = conn.cursor()

    for i in range(len(el.find_elements_by_tag_name('option'))): # iterate for the length of dropdown options
        el = browser.find_element_by_id('win0divUC_CLSRCH_WRK2_SUBJECTctrl') # avoid stale element exception
        el.find_elements_by_tag_name('option')[i+10].click()  # click a dropdown menu item
        submit = browser.find_element_by_id("UC_CLSRCH_WRK2_SEARCH_BTN") #avoid stale element exception
        submit.click() # submit department query
        value_wait = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ps_box-value")))
        try:
            flag = True
            while(flag):
                find = browser.find_element_by_id("win0divUC_RSLT_NAV_WRK_HTMLAREA$0")
                #w = wait.until(EC.element_to_be_clickable((By.ID, "win0divUC_RSLT_NAV_WRK_HTMLAREA$0")))
                sleep(5)
                class_desc= browser.find_elements_by_css_selector("tr.ps_grid-row.psc_rowact")
                for clas in class_desc:
                    print(clas.text)
                for j in range(len(class_desc[1:-4])):
                    print(len(class_desc[1:-4]))
                    find = browser.find_element_by_id("win0divUC_RSLT_NAV_WRK_HTMLAREA$0")
                    w = wait.until(EC.element_to_be_clickable((By.ID, "win0divUC_RSLT_NAV_WRK_HTMLAREA$0")))
                    w2 = wait.until(EC.invisibility_of_element_located((By.ID, "WAIT_win0")))
                    class_descs = browser.find_elements_by_css_selector("tr.ps_grid-row.psc_rowact")
                    w3 = wait.until(EC.element_to_be_clickable((By.ID, "DESCR100$0_row_0")))
                    class_descs[j].click()
                    desc_wait = wait.until(EC.presence_of_element_located((By.ID, "UC_CLS_DTL_WRK_DESCRLONG$0")))
                        
                    html = browser.page_source
                    soup = bs4.BeautifulSoup(html, "lxml")

                    class_dict = get_course_info(soup, j)
                    sql_commit_(class_dict)
                    #list_of_class_dicts.append(class_dict)
                    #c.execute("INSERT INTO employees (first_name) VALUES (%s)", ('Jane'))
                    #cnx.commit()
                    
                    ret = wait.until(EC.visibility_of_element_located((By.ID, "UC_CLS_DTL_WRK_RETURN_PB$0")))
                    ret_btn = browser.find_element_by_id("UC_CLS_DTL_WRK_RETURN_PB$0")
                    ret_btn.click()
                try:
                    more_wait =  WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.ID, "UC_RSLT_NAV_WRK_SEARCH_CONDITION2$46$")))
                    more_results = browser.find_element_by_id("UC_RSLT_NAV_WRK_SEARCH_CONDITION2$46$") # see if page has more than 25 results
                    more_results.click() # bring up next 25 results
           
                except NoSuchElementException: # continue if page has no more results to load
                    flag= False
                except TimeoutException:
                    break
        except NoSuchElementException: 
            continue
    browser.quit()

    return list_of_class_dicts


def create_course_csv(list_of_class_dicts, index_filename):
    keys = list_of_class_dicts[0].keys()

    with open(index_filename, 'wb') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(list_of_class_dicts)

    return output_file

    ## This doesn't work yet....

def sql_commit_(class_dict):
    conn = sqlite3.connect("test.db")
    c = conn.cursor()

    l = ["CourseNum", "Dept", "Sect", "Desc","Title",
         "Times", "StartTime", "EndTime", "SectionEnroll",
          "TotalEnroll", "StartDate", "EndDate"]

    print(class_dict["CourseId"])
    c.execute("INSERT INTO CourseInfo (CourseId) VALUES (?)", (str(class_dict["CourseId"]),))
    for entry in class_dict:
        if entry in l:
            sql_query = '''UPDATE CourseInfo SET {} = "{}" WHERE CourseId = "{}";'''.format(entry, class_dict[entry], class_dict['CourseId'])
            c.execute(sql_query)
        conn.commit()

    for prof in class_dict['Professors']:
        c.execute("INSERT INTO ProfTable (CourseId, Professor, Dept, CourseNum, Sect)\
                   VALUES (?, ?, ?, ?, ?)", (class_dict["CourseId"], 
                                            prof, class_dict["Dept"],
                                            class_dict["CourseNum"], 
                                            class_dict["Sect"]))
        conn.commit()




make_table()
create_list()
def me():
    CourseInfo = "CREATE TABLE CourseInfo(\
        CourseId INT(10000) Primary Key,\n\
        Dept VARCHAR(4),\n\
        CourseNum TEXT,\n\
        Sect TEXT,\n\
        Title TEXT,\n\
        Desc TEXT,\n\
        Days VARCHAR(100),\n\
        StartTime INT,\n\
        EndTime INT,\n\
        SectionEnroll VARCHAR(10),\n\
        TotalEnroll VARCHAR(10),\n\
        StartDate VARCHAR(15),\n\
        EndDate VARCHAR(15));"
    
    ProfTable = "CREATE TABLE ProfTable(\
                CourseId INT(10000),\n\
                Professor VARCHAR(1000),\n\
                Dept VARCHAR(4),\n\
                CourseNum TEXT,\n\
                Sect TEXT);"

    MeetingPatterns = "CREATE TABLE MeetingPatterns(\
                        CourseId INT(10000)\
                        Days VARCHAR(100),\n\
                        Times INT(2400),\n\
                        StartTime TEXT,\n\
                        EndTime TEXT,\n\
                        StartDate VARCHAR(15),\n\
                        EndDate VARCHAR(15));"