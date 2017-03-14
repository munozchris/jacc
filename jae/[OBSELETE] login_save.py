# note that this solution doesn't work - keeps returning invalid domain error
# alternative solution using this code that could work is to just pass the driver
# with the authenticated session (second function)

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from getpass import getpass
import requests

url1 = 'https://evaluations.uchicago.edu/index.php?EvalSearchType=option-number-search&Department=&CourseDepartment=AKKD&CourseNumber=10102&InstructorLastName=&advancedSearch=SEARCH'
url2 = 'https://evaluations.uchicago.edu/index.php?EvalSearchType=option-dept-search&Department=BIOS&AcademicYear=2016&CourseDepartment=&CourseNumber=&InstructorLastName=&advancedSearch=SEARCH'
url3 = 'https://aisweb.uchicago.edu/psp/ihprd/EMPLOYEE/EMPL/s/WEBLIB_REDIRECT.ISCRIPT2.FieldFormula.IScript_redirect'
url4 = 'https://shibboleth2.uchicago.edu/idp/profile/SAML2/Redirect/SSO?execution=e1s1'

def get_cookies(url):

    driver = webdriver.Chrome()
    driver.get(url)

    # Fill the login form and submit it
    un = input("Please enter your CNETID here: ")
    driver.find_element_by_id('username').send_keys(un)
    pw = getpass('Please enter your my.UChicago password here: ')
    driver.find_element_by_id('password').send_keys(pw)
    driver.find_element_by_class_name('form-button').click()

    # cookies = {i['name']: i['value'] for i in driver.get_cookies()}
    cookies = driver.get_cookies()
    driver.quit()

    # formatted_cookies = []
    # for cookie_dict in cookies:
    #     formatted_cookies.append({'name':cookie_dict['name'], 'value':cookie_dict['value']})

    # return formatted_cookies

    return cookies



def get_auth_driver(url):
    driver = webdriver.Chrome()
    driver.get(url)

    # Fill the login form and submit it
    un = input("Please enter your CNETID here: ")
    driver.find_element_by_id('username').send_keys(un)
    pw = getpass('Please enter your my.UChicago password here: ')
    driver.find_element_by_id('password').send_keys(pw)
    driver.find_element_by_class_name('form-button').click()

    return driver

