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
import bs4  

url = 'https://coursesearch.uchicago.edu/psc/prdguest/EMPLOYEE/HRMS/c/UC_STUDENT_RECORDS_FL.UC_CLASS_SEARCH_FL.GBL'
browser = webdriver.Chrome()  
browser.get(url)
 
el = browser.find_element_by_id('win0divUC_CLSRCH_WRK2_SUBJECTctrl') # find the dropdown menu
submit = browser.find_element_by_id("UC_CLSRCH_WRK2_SEARCH_BTN") # find the submit button
wait = WebDriverWait(browser, 10)


for i in range(len(el.find_elements_by_tag_name('option'))): # iterate for the length of dropdown options
    el = browser.find_element_by_id('win0divUC_CLSRCH_WRK2_SUBJECTctrl') # avoid stale element exception
    el.find_elements_by_tag_name('option')[i+4].click()  # click a dropdown menu item
    submit = browser.find_element_by_id("UC_CLSRCH_WRK2_SEARCH_BTN") #avoid stale element exception
    submit.click() # submit department query
    value_wait = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ps_box-value")))
    new_page = browser.page_source # get JavaScript-rendered HTML
    #soup = bs4.BeautifulSoup(new_page, "lxml")
    #course_info = soup.find_all(class_="ps_box-value") # scrape and print course info
    #for detail in course_info:
        #print(detail.text)
    sleep(5)
    try:
        flag = True
        while(flag):
            class_desc= browser.find_elements_by_css_selector("tr.ps_grid-row.psc_rowact")
            for j in range(len(class_desc[1:-4])):
                find = browser.find_element_by_id("win0divUC_RSLT_NAV_WRK_HTMLAREA$0")
                w = wait.until(EC.element_to_be_clickable((By.ID, "win0divUC_RSLT_NAV_WRK_HTMLAREA$0")))
                w2 = wait.until(EC.invisibility_of_element_located((By.ID, "WAIT_win0")))
                class_descs = browser.find_elements_by_css_selector("tr.ps_grid-row.psc_rowact")
                class_descs[j].click()
                desc_wait = wait.until(EC.presence_of_element_located((By.ID, "UC_CLS_DTL_WRK_DESCRLONG$0")))
                new_page_desc = browser.page_source
                soup1 = bs4.BeautifulSoup(new_page_desc, "lxml")
                course_info = soup1.find(id="UC_CLS_DTL_WRK_DESCRLONG$0")
                ret = wait.until(EC.visibility_of_element_located((By.ID, "UC_CLS_DTL_WRK_RETURN_PB$0")))
                ret_btn = browser.find_element_by_id("UC_CLS_DTL_WRK_RETURN_PB$0")
                ret_btn.click()
            try:
                more_wait = wait.until(EC.visibility_of_element_located((By.ID, "UC_RSLT_NAV_WRK_SEARCH_CONDITION2$46$")))
                more_results = browser.find_element_by_id("UC_RSLT_NAV_WRK_SEARCH_CONDITION2$46$") # see if page has more than 25 results
                more_results.click() # bring up next 25 results
                sleep(5) # wait for page to load html
                #new_page = browser.page_source # get html from new page
                #soup = bs4.BeautifulSoup(new_page, "lxml")
                #course_info = soup.find_all(class_="ps_box-value")
                #for detail in course_info:
                    #print(detail.text)
            except NoSuchElementException: # continue if page has no more results to load
                flag= False
            except TimeoutException:
                break
    except NoSuchElementException: # continue if page has no more results to load
        continue
browser.quit()