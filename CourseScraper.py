from selenium import webdriver  
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep
import bs4  

url = 'https://coursesearch.uchicago.edu/psc/prdguest/EMPLOYEE/HRMS/c/UC_STUDENT_RECORDS_FL.UC_CLASS_SEARCH_FL.GBL'
browser = webdriver.Chrome()  
browser.get(url)
 
el = browser.find_element_by_id('win0divUC_CLSRCH_WRK2_SUBJECTctrl') # find the dropdown menu
submit = browser.find_element_by_id("UC_CLSRCH_WRK2_SEARCH_BTN") # find the submit button

for i in range(len(el.find_elements_by_tag_name('option'))): # iterate for the length of dropdown options
    el = browser.find_element_by_id('win0divUC_CLSRCH_WRK2_SUBJECTctrl') # avoid stale element exception
    el.find_elements_by_tag_name('option')[i+1].click()  # click a dropdown menu item
    submit = browser.find_element_by_id("UC_CLSRCH_WRK2_SEARCH_BTN") #avoid stale element exception
    submit.click() # submit department query
    sleep(15) # wait for page to load html
    #new_page = browser.page_source # get JavaScript-rendered HTML
    #soup = bs4.BeautifulSoup(new_page, "lxml")
    #course_info = soup.find_all(class_="ps_box-value") # scrape and print course info
    #for detail in course_info:
        #print(detail.text)
    try:
        flag = True
        while(flag):
            class_desc= browser.find_elements_by_css_selector("tr.ps_grid-row.psc_rowact")
            for j in range(len(class_desc[1:-4])):
                class_descs = browser.find_elements_by_css_selector("tr.ps_grid-row.psc_rowact")
                class_descs[j].click()
                sleep(5)
                new_page_desc = browser.page_source
                soup1 = bs4.BeautifulSoup(new_page_desc, "lxml")
                course_info = soup1.find(id="UC_CLS_DTL_WRK_DESCRLONG$0")
                print(course_info.text)
                ret_btn = browser.find_element_by_id("UC_CLS_DTL_WRK_RETURN_PB$0")
                ret_btn.click()
                sleep(5)
            try:
                more_results = browser.find_element_by_id("UC_RSLT_NAV_WRK_SEARCH_CONDITION2$46$") # see if page has more than 25 results
                more_results.click() # bring up next 25 results
                sleep(5) # wait for page to load html
                #new_page = browser.page_source # get html from new page
                #soup = bs4.BeautifulSoup(new_page, "lxml")
                #course_info = soup.find_all(class_="ps_box-value")
                #for detail in course_info:
                    #print(detail.text)
            except NoSuchElementException: # continue if page has no more results to load
                print('inner try')
                flag= False
    except NoSuchElementException: # continue if page has no more results to load
        print('outter try')
        continue