from selenium import webdriver  
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep



import bs4  

url = 'https://coursesearch.uchicago.edu/psc/prdguest/EMPLOYEE/HRMS/c/UC_STUDENT_RECORDS_FL.UC_CLASS_SEARCH_FL.GBL'
browser = webdriver.Chrome()  
browser.get(url)

el = browser.find_element_by_id('win0divUC_CLSRCH_WRK2_SUBJECTctrl')

for option in el.find_elements_by_tag_name('option'):
    if option.text == 'American Culture':
        option.click()
        break

sub = browser.find_element_by_id("UC_CLSRCH_WRK2_SEARCH_BTN")
new = sub.click()
sleep(5)
new = browser.page_source
browser.quit()
soup = bs4.BeautifulSoup(new, "lxml")

bb = soup.find_all(class_="ps_box-value")

for tag in bb:
    print(tag.text)


