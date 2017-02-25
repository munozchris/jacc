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


'''def make_table():
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    t = "DROP TABLE CourseInfo;"
    j = "CREATE TABLE CourseInfo(\
        CourseId VARCHAR(100) Primary Key,\
        CourseNum TEXT,\
        Dept VARCHAR(100),\
        Sect TEXT,\
        Desc TEXT,\
        Title TEXT,\
        Professors VARCHAR(1000),\
        Days VARCHAR(100),\
        Times INT(2400),\
        StartTime TEXT,\
        EndTime TEXT);"
    c.execute(t)
    c.execute(j)
    c.close()

'''


def get_course_info(soup, index):
    '''
    Given the page source in beautiful Soup format,
    returns a dictionary of all the info from the page
    '''

    l = ["CourseId", "CourseNum", "Dept", "Sect", "Desc","Title", "Professors",
         "Days", "StartTime", "EndTime"]


    class_info_dict = {"Professors": [], "Days1": [], "Days2": [], "CourseId": None, "Dept": None, "Title": None,
                        "CourseNum": None, "Sect": None, "Desc": None, "StartTime1": None,
                        "StartTime2": None, "EndTime1": None, "Endtime2": None, "StartDate": None,
                        "EndDate": None, "EvalLinks": []}

    # Get course title
    course_title = soup.find(class_="ps_box-value", id="UC_CLSRCH_WRK_UC_CLASS_TITLE$"+str(index))
    class_info_dict["Title"] = course_title.text

    # Get department, course number, section number, and course ID
    intermediate_list = soup.find_all(class_=["label label-success", "label label-default"])
    for item in intermediate_list:
        print(item.text)
    intermediate = intermediate_list[index]
    information = intermediate.parent.text
    print(information)
    dept = re.search("[A-Z]{4}", information)
    course_nums = re.findall("[0-9]{5}", information)
    course_num = course_nums[0]
    course_id = course_nums[1]
    section_num = re.search("[0-9]* ", information)

    class_info_dict["CourseNum"] = course_num
    class_info_dict["Dept"] = dept.group()
    class_info_dict["Sect"] = section_num.group().strip()
    class_info_dict["CourseId"] = course_id


    total_enrollment = soup.find(class_="ps_box-value", id="UC_CLSRCH_WRK_DESCR2$"+str(index))
    if total_enrollment is not None:
        total_enrollment = total_enrollment.text
        total_current = re.findall("[\d]+", total_enrollment)
        current = total_current[0]
        total = total_current[1]
        class_info_dict["Current Enrollment"] = int(current)
        class_info_dict["Total Enrollment"] = int(total)

     
    section_enrollment = soup.find(class_="ps_box-value", id="UC_CLSRCH_WRK_DESCR1$"+str(index))
    if section_enrollment is not None:
        section_enrollment = section_enrollment.text
        total_current = re.findall("[\d]+", section_enrollment)
        current = total_current[0]
        total = total_current[1]


        #current_enrollment = re.search("[\d]+\/", section_enrollment).group()
        #current_enrollment = current_enrollment[:-1]
        #total_enrollment = re.search("^\/[\d]+", section_enrollment).group()
        #total_enrollment = total_enrollment[1:]
        class_info_dict["Current Section Enrollment"] = int(current)
        class_info_dict["Total Section Enrollment"] = int(total)


    prof = soup.find(class_="ps_box-value", id="MTG$0")
    text = prof.text
    all_profs = re.findall("[^,]+", text)
    for professor in all_profs:
        class_info_dict["Professors"].append(professor.strip())


    times_and_days = soup.find_all(class_="ps_box-value", id=["MTG_SCHED$0", "MTG_SCHED$1"])

    if len(times_and_days) == 1:

        times_and_days = soup.find(class_="ps_box-value", id="MTG_SCHED$0")
        text = times_and_days.text

        days = re.findall("[A-Z][a-z]+", text)
        for day in days:
            class_info_dict["Days1"].append(day)

        times = re.findall("[0-9][0-9]:[0-9][0-9] [A-Z][A-Z]", text)

        if len(times) == 2:

            start_time = times[0]
            hour = start_time[:2]
            minute = start_time[3:5]
            if start_time[6:] == "PM" and hour != "12":
                hour = str(int(hour)+12)
            start_time = int(hour+minute)
            class_info_dict["StartTime1"] = start_time

            end_time = times[1]
            hour = end_time[:2]
            minute = end_time[3:5]
            if end_time[6:] == "PM":
                hour = str(int(hour)+12)
            end_time = int(hour+minute)
            class_info_dict["EndTime1"] = end_time

    elif len(times_and_days) > 1:

        count = 0

        for box in times_and_days:
            text = box.text
            count += 1

            days = re.findall("[A-Z][a-z]+", text)
            for day in days:
                class_info_dict["Days"+str(count)].append(day)

            times = re.findall("[0-9][0-9]:[0-9][0-9] [A-Z][A-Z]", text)

            if len(times) == 2:

                start_time = times[0]
                hour = start_time[:2]
                minute = start_time[3:5]
                if start_time[6:] == "PM" and hour != "12":
                    hour = str(int(hour)+12)
                start_time = int(hour+minute)
                class_info_dict["StartTime"+str(count)] = start_time

                end_time = times[1]
                hour = end_time[:2]
                minute = end_time[3:5]
                if end_time[6:] == "PM":
                    hour = str(int(hour)+12)
                end_time = int(hour+minute)
                class_info_dict["EndTime"+str(count)] = end_time


    timeframe = soup.find(class_="ps_box-value", id="MTG_DATE$0")
    text = timeframe.text
    print(text)
    start_date = text[:10]
    print(start_date)
    end_date = text[13:]
    print(end_date)
    class_info_dict["StartDate"] = start_date
    class_info_dict["EndDate"] = end_date


    description = soup.find(class_="ps_box-value", id="UC_CLS_DTL_WRK_DESCRLONG$0")
    text = description.text
    class_info_dict["Desc"] = text

    evals = soup.find(class_="ps_box-htmlarea", id="win0divUC_CLSRCH_WRK_HTMLAREA2$0")
    print(evals)
    #evals = evals.child.child.child
    #text = evals.text
    #class_info_dict["EvalLinks"] = text

    
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
    wait = WebDriverWait(browser, 15)

    list_of_class_dicts = []

    #conn = sqlite3.connect(sql_filename)
    #c = conn.cursor()

    #for i in range(len(el.find_elements_by_tag_name('option'))): # iterate for the length of dropdown options
    for i in range(10,11): 
        el = browser.find_element_by_id('win0divUC_CLSRCH_WRK2_SUBJECTctrl') # avoid stale element exception
        el.find_elements_by_tag_name('option')[i+1].click()  # click a dropdown menu item
        submit = browser.find_element_by_id("UC_CLSRCH_WRK2_SEARCH_BTN") #avoid stale element exception
        submit.click() # submit department query
        value_wait = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ps_box-value")))
        try:
            flag = True
            while(flag):
                find = browser.find_element_by_id("win0divUC_RSLT_NAV_WRK_HTMLAREA$0")
                sleep(5)
                #w = wait.until(EC.element_to_be_clickable((By.ID, "win0divUC_RSLT_NAV_WRK_HTMLAREA$0")))
                class_desc= browser.find_elements_by_css_selector("tr.ps_grid-row.psc_rowact")
                for j in range(len(class_desc[1:-4])):
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
                    print(class_dict)
                   # sql_commit_(class_dict)
                    #list_of_class_dicts.append(class_dict)
                    #c.execute("INSERT INTO employees (first_name) VALUES (%s)", ('Jane'))
                    #cnx.commit()
                    
                    ret = wait.until(EC.visibility_of_element_located((By.ID, "UC_CLS_DTL_WRK_RETURN_PB$0")))
                    ret_btn = browser.find_element_by_id("UC_CLS_DTL_WRK_RETURN_PB$0")
                    ret_btn.click()
                try:
                    more_wait = wait.until(EC.visibility_of_element_located((By.ID, "UC_RSLT_NAV_WRK_SEARCH_CONDITION2$46$")))
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

class_list = create_list()

'''
def sql_commit_(class_dict):
    conn = sqlite3.connect("test.db")
    c = conn.cursor()

    l = ["CourseNum", "Dept", "Sect", "Desc","Title", "Professors",
         "Days", "Times", "StartTime", "EndTime"]

    print(class_dict["CourseId"])
    c.execute("INSERT INTO CourseInfo (CourseId) VALUES (?)", (str(class_dict["CourseId"]),))
    for entry in class_dict:
        print(entry)
        if entry in l and len(class_dict[entry]) > 0:
            if type(entry) == list: 
                entry = str(tuple(entry))
            if type(class_dict[entry]) == list: 
                class_dict[entry] = str(class_dict[entry][0])
            sql_query = "UPDATE CourseInfo SET" + " " + entry + "= " +\
                    "'"  + class_dict[entry] + "'" +\
                    " WHERE CourseId =" + "'" + str(class_dict['CourseId']) + "'" + ";"
            print(sql_query)
            c.execute(sql_query)
        conn.commit()

make_table()
create_list()

'''
