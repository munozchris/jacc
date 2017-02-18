from selenium import webdriver  
from selenium.common.exceptions import NoSuchElementException  
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from time import sleep
import bs4 
import re

url = "https://coursesearch.uchicago.edu/psc/prdguest/EMPLOYEE/HRMS/c/UC_STUDENT_RECORDS_FL.UC_CLASS_SEARCH_FL.GBL"

#driver = webdriver.Chrome("/usr/local/bin/chromedriver")
browser = webdriver.Chrome()
browser.get(url)

el = browser.find_element_by_id('win0divUC_CLSRCH_WRK2_SUBJECTctrl')
submit = browser.find_element_by_id("UC_CLSRCH_WRK2_SEARCH_BTN")

el.find_elements_by_tag_name('option')[9].click()
submit = browser.find_element_by_id("UC_CLSRCH_WRK2_SEARCH_BTN") #avoid stale element exception
submit.click() # submit department query
sleep(15) # wait for page to load html

list_of_class_dicts = []
    
try:
    flag = True
    while(flag):
        find = browser.find_element_by_id("win0divUC_RSLT_NAV_WRK_HTMLAREA$0")
        class_desc = browser.find_elements_by_css_selector("tr.ps_grid-row.psc_rowact")
        # assume len(class_desc[1:-4]) = how many classes are on the page

        for j in range(len(class_desc[1:-4])):
            sleep(15)
            class_descs = browser.find_elements_by_css_selector("tr.ps_grid-row.psc_rowact")
            class_descs[j].click()
            sleep(5)

            html = browser.page_source
            soup = bs4.BeautifulSoup(html, "lxml")

            class_info_dict = {"Course Title": None, "Course Number": None, "Total Enrollment": None, 
                                "Section Enrollment": None, "Professors": [], "Days": [], 
                                "Start Time": None, "End Time": None, "Timeframe": None}

            course_title = soup.find(class_="ps_box-value", id="UC_CLSRCH_WRK_UC_CLASS_TITLE$"+str(j))
            class_info_dict["Course Title"] = course_title.text

            
            #lolll
            intermediate = soup.find(class_="label label-success")
            information = intermediate.parent.text
            dept = information[:4]
            course_num = information[5:10]
            section_num = information[11]
            course_id = information[14:19]

            ## this assumes that all department codes are 4 letters

            class_info_dict["Course Number"] = course_num
            class_info_dict["Dept"] = dept
            class_info_dict["Section"] = section_num
            class_info_dict["Course ID"] = course_id

            
            #if: regular expression saying that it exists
            total_enrollment = soup.find(class_="ps_box-value", id="UC_CLSRCH_WRK_DESCR2$"+str(j))
            text = total_enrollment.text
            numbers = text[18:]
            class_info_dict["Total Enrollment"] = numbers
     

            #if: regular expression saying that it exists
            section_enrollment = soup.find(class_="ps_box-value", id="UC_CLSRCH_WRK_DESCR1$"+str(j))
            text = section_enrollment.text
            numbers = text[20:]
            class_info_dict["Section Enrollment"] = numbers

            prof = soup.find(class_="ps_box-value", id="MTG$0")
            text = prof.text
            all_profs = re.findall("[A-Z a-z]", text)
            ### ahh need help with this reg ex
            ### basically i'd like to keep going until you hit a comma
            ### [^,] ??
            for professor in all_profs:
                class_info_dict["Professors"].append(professor)


            times_and_day = soup.find(class_="ps_box-value", id="MTG_SCHED$0")
            text = times_and_day.text

            days = re.findall("[A-Z][a-z]+", text)
            for day in days:
                class_info_dict["Days"].append(day)

            times = re.findall("[0-9][0-9]:[0-9][0-9] [A-Z][A-Z]", text)

            start_time = times[0]
            hour = start_time[:2]
            minute = start_time[3:5]
            if start_time[6:] == "PM":
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

            time_frame = soup.find(class_="ps_box-value", id="MTG_DATE$0")
            class_info_dict["Timeframe"] = time_frame.text
    
            list_of_class_dicts.append(class_info_dict)
            print(class_info_dict)

            sleep(15)


            ret_btn = browser.find_element_by_id("UC_CLS_DTL_WRK_RETURN_PB$0")
            ret_btn.click()
     
except NoSuchElementException: # continue if page has no more results to load
    print('outter try')
