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


# Running this file will create a database, scrape all the relevant 
# course information, and store all that information in the database


def make_table():
    '''
    This function makes our SQLite database to hold course information 
    for a certain quarter. If the tables already exist, it drops them 
    and starts over.
    '''

    conn = sqlite3.connect("winter.db") # when we ran it, the database 
                                        # was called "test"
    c = conn.cursor()
    t = "DROP TABLE IF EXISTS CourseInfo;"
    t2 = "DROP TABLE IF EXISTS ProfTable;"
    t3 = "DROP TABLE IF EXISTS SectionInfo"
    t4 = "DROP TABLE IF EXISTS Description"

    CourseInfo = "CREATE TABLE CourseInfo(\n\
        CourseId INT(10000) Primary Key,\n\
        Dept VARCHAR(4),\n\
        CourseNum TEXT,\n\
        Title TEXT,\n\
        EvalLinks TEXT,\n\
        TotalEnroll INT(10),\n\
        CurrentTotalEnroll INT(10),\n\
        StartDate VARCHAR(15),\n\
        EndDate VARCHAR(15));"

    SectionInfo = "CREATE TABLE SectionInfo(\n\
            SectionId INT(10000) Primary Key,\n\
            CourseId INT(10000),\n\
            Sect TEXT,\n\
            Professor TEXT,\n\
            Days1 VARCHAR(100),\n\
            Days2 VARCHAR(100),\n\
            StartTime1 INT,\n\
            StartTime2 INT,\n\
            EndTime1 INT,\n\
            EndTime2 INT,\n\
            SectionEnroll INT(10),\n\
            CurrentSectionEnroll INT(10));"
    
    
    ProfTable = "CREATE TABLE ProfTable(\n\
                Professor VARCHAR(1000),\n\
                CourseId INT(10000),\n\
                SectionId INT(1000));"


    DescTable = "CREATE TABLE Description(\n\
                        CourseId INT(10000),\n\
                        Description TEXT);"


    c.execute(t)
    c.execute(t2)
    c.execute(t3)
    c.execute(t4)
    c.execute(CourseInfo)
    c.execute(SectionInfo)
    c.execute(ProfTable)
    c.execute(DescTable)
    c.close()



def get_course_info(soup, index):
    '''
    Given the page source for a class in BeautifulSoup format, this function
    returns a dictionary of all the relevant course info from the page. It 
    also takes an index, which refers to where the course lies in a list of all
    courses on the main page of courses for a department. 
    '''

    l = ["CourseId", "CourseNum", "Dept", "Sect", "Description","Title", 
            "Professors", "Days1", "Days2" "StartTime1", "StartTime2" 
            "EndTime1", "EndTime2", "EvalLinks"]


    class_info_dict = {"Professors": [], "Days1": None, "Days2": None, 
                        "CourseId": None, "SectionId": None, "Dept": None, 
                        "Title": None, "CourseNum": None, "Sect": None, 
                        "Description": None, "StartTime1": None, "StartTime2":
                        None, "EndTime1": None, "EndTime2": None, "StartDate": 
                        None, "EndDate": None, "EvalLinks": [], "TotalEnrollment": 
                        None, "CurrentTotalEnrollment": None, "SectionEnrollment": 
                        None, "TotalSectionEnrollment": None}



    # Find the class title, add it to the dictionary
    course_title = soup.find(class_="ps_box-value", 
                            id="UC_CLSRCH_WRK_UC_CLASS_TITLE$"+str(index))
    if course_title is not None:
        class_info_dict["Title"] = course_title.text


    # Use Beautiful Soup to find department, course number, section number,
    # and course ID in html

    intermediate_list = soup.find_all(class_=["label label-success", 
                                        "label label-default", 
                                        "label label-danger", 
                                        "label label-warning"])

    # Now use Regular Expressions to find each individual piece of 
    # information

    if len(intermediate_list) != 0:
        intermediate = intermediate_list[index]
        information = intermediate.parent.text
        dept = re.search("[A-Z]{4}", information).group()
        course_nums = re.findall("[0-9]{5}", information)
        course_num = course_nums[0]
        section_id = course_nums[1]
        section_num = re.search("[0-9]+ ", information)


    # Put that information into the dictionary

    if course_num is not None:
        class_info_dict["CourseNum"] = course_num
    if dept is not None:
        class_info_dict["Dept"] = dept
    if section_num is not None:
        class_info_dict["Sect"] = section_num.group().strip()
    if section_id is not None:
        class_info_dict["SectionId"] = section_id


    # Create a "CourseId" that refers to a department and course
    # number that can be used as the unique key in the database.
    # Assign a number to each letter and put it together with the
    # course number to create a unique dept-number code


    dept_code = ""
    for letter in dept:
        dept_code += str(ord(letter))
    course_id = dept_code + course_num
    course_id = int(course_id)
    class_info_dict["CourseId"] = course_id


    # Find the total enrollment for the course, the current enrollment,
    # the total section enrollment for each section, and the current
    # enrollment in each section

    total_enrollment = soup.find(class_="ps_box-value", 
                                id="UC_CLSRCH_WRK_DESCR2$"+str(index))
    if total_enrollment is not None:
        total_enrollment = total_enrollment.text
        total_current = re.findall("[\d]+", total_enrollment)
        if len(total_current) != 0:
            current = total_current[0]
            total = total_current[1]
            class_info_dict["CurrentTotalEnrollment"] = int(current)
            class_info_dict["TotalEnrollment"] = int(total)

     
    section_enrollment = soup.find(class_="ps_box-value", 
                                id="UC_CLSRCH_WRK_DESCR1$"+str(index))
    if section_enrollment is not None:
        section_enrollment = section_enrollment.text
        total_current = re.findall("[\d]+", section_enrollment)
        if len(total_current) != 0:
            current = total_current[0]
            total = total_current[1]
            class_info_dict["CurrentSectionEnrollment"] = int(current)
            class_info_dict["TotalSectionEnrollment"] = int(total)

    # Find the timeframe, ie the dates the course will be taught. 
    # (Essentially the dates of the quarter)

    timeframe = soup.find(class_="ps_box-value", id="MTG_DATE$0")
    if timeframe is not None:
        text = timeframe.text
        start_date = text[:10]
        end_date = text[13:]
        class_info_dict["StartDate"] = start_date
        class_info_dict["EndDate"] = end_date

    # Find the professors and add them to a list, then add that list 
    # to the dictionary
    
    prof = soup.find(class_="ps_box-value", id="MTG$0")
    if prof is not None:
        text = prof.text
        all_profs = re.findall("[^,]+", text)
        for professor in all_profs:
            class_info_dict["Professors"].append(professor.strip())


    # Find the times and days of the week that the class is taught

    times_and_days = soup.find_all(class_="ps_box-value", id=["MTG_SCHED$0", 
                                                    "MTG_SCHED$1"])

    # Some classes are taught at different times a few days a week, so we need 
    # to separate them into two different options if that is the case

    if len(times_and_days) == 1:

        times_and_days = soup.find(class_="ps_box-value", id="MTG_SCHED$0")
        text = times_and_days.text

        # Make a string of letters, each letter signifying a day of the week

        days = re.findall("[A-Z][a-z]+", text)
        day_string = ""
        for day in days:
            if day[0] != "T":
                day_string += day[0]
            if day == "Tues":
                day_string += "T"
            if day == "Thu":
                day_string += "R"
        class_info_dict["Days1"] = day_string

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
            if end_time[6:] == "PM" and hour != "12":
                hour = str(int(hour)+12)
            end_time = int(hour+minute)
            class_info_dict["EndTime1"] = end_time

    elif len(times_and_days) > 1:

        count = 0

        for box in times_and_days:
            text = box.text
            count += 1

            days = re.findall("[A-Z][a-z]+", text)
            day_string = ""
            for day in days:
                if day[0] != "T":
                    day_string += day[0]
                elif day == "Tues":
                    day_string += "T"
                elif day == "Thu":
                    day_string += "R"
            class_info_dict["Days"+str(count)] = day_string

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
                if end_time[6:] == "PM" and hour != "12":
                    hour = str(int(hour)+12)
                end_time = int(hour+minute)
                class_info_dict["EndTime"+str(count)] = end_time

    # Get the class description as a long string of text

    description = soup.find(class_="ps_box-value", 
                            id="UC_CLS_DTL_WRK_DESCRLONG$0")
    if description is not None:
        text = description.text
        class_info_dict["Description"] = text

    # Get the gateway url to the evaluations page

    evals = soup.find("a", onclick="window.open(this.href,'Evaluations'); return false;")["href"]
    if evals is not None:
        class_info_dict["EvalLinks"] = evals
    
    return class_info_dict



def scrape():
    '''
    The function begins at the "home page" for class searches (under the 
    staff tab, so we don't have to log in). It then proceeds to go through 
    all departments, then all classes in each department, and scrapes all 
    the information from each of those classes. It calls the function 
    get_course_info to make a dictionary, then commmits that dictionary to 
    our SQLite database. 
    '''

    url = "https://coursesearch.uchicago.edu/psc/prdguest/EMPLOYEE/HRMS/c/UC_STUDENT_RECORDS_FL.UC_CLASS_SEARCH_FL.GBL"
    
    browser = webdriver.Chrome()  
    browser.get(url)


    el = browser.find_element_by_id('win0divUC_CLSRCH_WRK2_SUBJECTctrl') 
        # find the dropdown menu
    submit = browser.find_element_by_id("UC_CLSRCH_WRK2_SEARCH_BTN") 
        # find the submit button
    wait = WebDriverWait(browser, 10)

    # If we wanted to scrape Spring classes instead of Winter classes, 
    # we could do this:

    # select = Select(browser.find_element_by_id("UC_CLSRCH_WRK2_STRM"))
    # select.select_by_value('2174')
    # conn = sqlite3.connect(sql_filename)
    # c = conn.cursor()

    for i in range(2, len(el.find_elements_by_tag_name('option'))): 
            # iterate for the length of dropdown options 
            # (starting at the second one)
        el = browser.find_element_by_id('win0divUC_CLSRCH_WRK2_SUBJECTctrl') 
            # avoid stale element exception
        el.find_elements_by_tag_name('option')[i].click()  
            # click a dropdown menu item
        submit = browser.find_element_by_id("UC_CLSRCH_WRK2_SEARCH_BTN") 
            # avoid stale element exception
        submit.click() 
            # submit department query
        value_wait = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ps_box-value")))

        try:
            flag = True
            while(flag):
                find = browser.find_element_by_id("win0divUC_RSLT_NAV_WRK_HTMLAREA$0")
                sleep(5)
                class_desc= browser.find_elements_by_css_selector("tr.ps_grid-row.psc_rowact")
                for j in range(len(class_desc[1:-4])):
                        # for all classes, find the class and click on it
                    find = browser.find_element_by_id("win0divUC_RSLT_NAV_WRK_HTMLAREA$0")
                    sleep(3)
                    class_descs = browser.find_elements_by_css_selector("tr.ps_grid-row.psc_rowact")
                    sleep(3)
                    class_descs[j].click()
                    sleep(3)
                        
                    html = browser.page_source
                    soup = bs4.BeautifulSoup(html, "lxml")

                    # Get the Beautiful Soup and pass it to the function
                    # to get the dictionary

                    class_dict = get_course_info(soup, j)
                    sql_commit_(class_dict)

                    # Commit the dictionary to SQLite database
                 
                    ret = wait.until(EC.visibility_of_element_located((By.ID, "UC_CLS_DTL_WRK_RETURN_PB$0")))
                    ret_btn = browser.find_element_by_id("UC_CLS_DTL_WRK_RETURN_PB$0")
                    ret_btn.click()

                    # Go back to the previous page
                try:

                    # If there are more results (another page), click on it
                    # and do the same for the next page

                    more_wait =  WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.ID, "UC_RSLT_NAV_WRK_SEARCH_CONDITION2$46$")))
                    more_results = browser.find_element_by_id("UC_RSLT_NAV_WRK_SEARCH_CONDITION2$46$") 
                                # see if page has more than 25 results
                    more_results.click() 
                                # if it does, click next page
           
                except NoSuchElementException: # continue if page has no more 
                                               # results to load
                    flag= False
                except TimeoutException:
                    break
        except NoSuchElementException: 
            continue
    browser.quit()



def sql_commit_(class_dict):
    conn = sqlite3.connect("winter.db")
    c = conn.cursor()

    # Insert some values into the SectionInfo table

    sql_query = ("INSERT INTO SectionInfo (SectionId, CourseId, Sect,\
                    Professor, Days1, Days2, StartTime1, StartTime2, EndTime1,\
                    EndTime2, SectionEnroll, CurrentSectionEnroll)\
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")

    data = (class_dict["SectionId"], class_dict["CourseId"], class_dict["Sect"],
            str(class_dict["Professors"]), class_dict["Days1"], 
            class_dict["Days2"], str(class_dict["StartTime1"]), 
            str(class_dict["StartTime2"]), str(class_dict["EndTime1"]), 
            str(class_dict["EndTime2"]), str(class_dict["SectionEnrollment"]), 
            str(class_dict["CurrentSectionEnrollment"]))

    c.execute(sql_query, data)

    conn.commit()

    # Insert some values into the CourseInfo table

    sql_query = "INSERT OR REPLACE INTO CourseInfo (CourseId, CourseNum, Dept,\
                    Title, TotalEnroll, CurrentTotalEnroll, StartDate,\
                    EndDate, EvalLinks) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"

    data = (class_dict["CourseId"], class_dict["CourseNum"], 
            class_dict["Dept"], class_dict["Title"], 
            class_dict["TotalEnrollment"],
            class_dict["CurrentTotalEnrollment"], class_dict["StartDate"],
            class_dict["EndDate"], class_dict["EvalLinks"])

    c.execute(sql_query, data)

    conn.commit()


    # Insert some values into the ProfTable table
    # by iterating through the list of professors

    for prof in class_dict['Professors']:
        c.execute("INSERT INTO ProfTable (Professor, CourseId, SectionId)\
                   VALUES (?, ?, ?)", (prof, class_dict["CourseId"], 
                    class_dict["SectionId"]))                             
        
        conn.commit()

    # Insert some values into the Description table

    sql_query = "INSERT OR REPLACE INTO Description (CourseId, Description)\
                VALUES (?, ?)"

    c.execute(sql_query, (class_dict["CourseId"], class_dict["Description"]))

    conn.commit()


make_table()
scrape()
