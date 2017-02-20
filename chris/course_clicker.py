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
from login_save import get_auth_driver

import bs4  
import re
import csv

def get_course_info(soup, index):
    '''
    Given the page source in beautiful Soup format,
    returns a dictionary of all the info from the page
    '''

    class_info_dict = {"Professors": [], "Days": []}

    # Get course title
    course_title = soup.find(class_="ps_box-value", id="UC_CLSRCH_WRK_UC_CLASS_TITLE$"+str(index))
    class_info_dict["Course Title"] = course_title.text

    # Get department, course number, section number, and course ID
    intermediate = soup.find(class_="label label-success")
    information = intermediate.parent.text
    dept = re.search("[A-Z]{4}", information)
    course_nums = re.findall("[0-9]{5}", information)
    course_num = course_nums[0]
    course_id = course_nums[1]
    section_num = re.search("[0-9] ", information)

    class_info_dict["Course Number"] = course_num
    class_info_dict["Dept"] = dept.group()
    class_info_dict["Section"] = section_num.group()
    class_info_dict["Course ID"] = course_id

            
    #if it exists
    total_enrollment = soup.find(class_="ps_box-value", id="UC_CLSRCH_WRK_DESCR2$"+str(index))
    text = total_enrollment.text
    numbers = text[18:]
    class_info_dict["Total Enrollment"] = numbers
     
    # if it exists
    section_enrollment = soup.find(class_="ps_box-value", id="UC_CLSRCH_WRK_DESCR1$"+str(index))
    text = section_enrollment.text
    numbers = text[20:]
    class_info_dict["Section Enrollment"] = numbers

    prof = soup.find(class_="ps_box-value", id="MTG$0")
    text = prof.text
    all_profs = re.findall("[A-Z][A-Za-z\s]+", text)
    for professor in all_profs:
        class_info_dict["Professors"].append(professor)


    times_and_day = soup.find(class_="ps_box-value", id="MTG_SCHED$0")
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
        class_info_dict["Start Time"] = start_time

        end_time = times[1]
        hour = end_time[:2]
        minute = end_time[3:5]
        if end_time[6:] == "PM":
            hour = str(int(hour)+12)
        end_time = int(hour+minute)
        class_info_dict["End Time"] = end_time

    timeframe = soup.find(class_="ps_box-value", id="MTG_DATE$0")
    text = timeframe.text
    start_date = text[:10]
    end_date = text[13:]
    class_info_dict["Start Date"] = start_date
    class_info_dict["End Date"] = end_date
    
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
    browser = get_auth_driver(url2)
    browser.get(url)

    list_of_class_dicts = []


    for i in range(len(el.find_elements_by_tag_name('option'))): # iterate for the length of dropdown options
        el = browser.find_element_by_id('win0divUC_CLSRCH_WRK2_SUBJECTctrl') # avoid stale element exception
        el.find_elements_by_tag_name('option')[i].click()  # click a dropdown menu item
        submit = browser.find_element_by_id("UC_CLSRCH_WRK2_SEARCH_BTN") #avoid stale element exception
        submit.click() # submit department query
        value_wait = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ps_box-value")))
        try:
            flag = True
            while(flag):
                w = wait.until(EC.element_to_be_clickable((By.ID, "win0divUC_RSLT_NAV_WRK_HTMLAREA$0")))
                class_desc= browser.find_elements_by_css_selector("tr.ps_grid-row.psc_rowact")
                for j in range(len(class_desc[1:-4])):
                    find = browser.find_element_by_id("win0divUC_RSLT_NAV_WRK_HTMLAREA$0")
                    w = wait.until(EC.element_to_be_clickable((By.ID, "win0divUC_RSLT_NAV_WRK_HTMLAREA$0")))
                    w2 = wait.until(EC.invisibility_of_element_located((By.ID, "WAIT_win0")))
                    class_descs = browser.find_elements_by_css_selector("tr.ps_grid-row.psc_rowact")
                    class_descs[j].click()
                    desc_wait = wait.until(EC.presence_of_element_located((By.ID, "UC_CLS_DTL_WRK_DESCRLONG$0")))
                        
                    html = browser.page_source
                    soup = bs4.BeautifulSoup(html, "lxml")

                    class_dict = get_course_info(soup, j)
                    print(class_dict)
                    list_of_class_dicts.append(class_dict)
                    
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
        except NoSuchElementException: # continue if page has no more results to load
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

create_list()


# Maybe ideally this would do both things at once -- it would run through the course
# website, and instead of creating a list of dictionaries it would just add all the 
# info to a csv file. Creating a list is probably an inefficient intermediate 
# step but I'm not sure at this point how to skip it...