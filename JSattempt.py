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

el = browser.find_element_by_id('win0divUC_CLSRCH_WRK2_SUBJECTctrl')
submit = browser.find_element_by_id("UC_CLSRCH_WRK2_SEARCH_BTN")

for i in range(len(el.find_elements_by_tag_name('option'))):
    el = browser.find_element_by_id('win0divUC_CLSRCH_WRK2_SUBJECTctrl')
    el.find_elements_by_tag_name('option')[i].click()
    submit = browser.find_element_by_id("UC_CLSRCH_WRK2_SEARCH_BTN")
    submit.click()
    sleep(15)
    new_page = browser.page_source
    soup = bs4.BeautifulSoup(new_page, "lxml")
    course_info = soup.find_all(class_="ps_box-value")
    for detail in course_info:
        print(detail.text)
    try:
        more_results = browser.find_element_by_id("UC_RSLT_NAV_WRK_SEARCH_CONDITION2$46$")
        while more_results:
            more_results.click()
            sleep(5)
            new_page = browser.page_source
            soup = bs4.BeautifulSoup(new_page, "lxml")
            course_info = soup.find_all(class_="ps_box-value")
            for detail in course_info:
                print(detail.text)
            more_results = browser.find_element_by_id("UC_RSLT_NAV_WRK_SEARCH_CONDITION2$46$")
    except NoSuchElementException:
        continue