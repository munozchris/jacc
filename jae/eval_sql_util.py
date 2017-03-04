# Auxiliary function to filter out irrelevant evaluations by year 
# Tag finder code copied from Jae's code

from selenium import webdriver  
import bs4
from login_save import get_auth_driver
import urllib.parse
import re
import requests
from requests.auth import HTTPBasicAuth
from getpass import getpass
    
    

# driver = webdriver.Chrome("/usr/local/bin/chromedriver")
    
# threshold_year = 2011
# url2 = 'https://evaluations.uchicago.edu/index.php?EvalSearchType=option-number-search&Department=&CourseDepartment=AKKD&CourseNumber=10102&InstructorLastName=&advancedSearch=SEARCH'
# browser = get_auth_driver(url2)

# url3 = 'https://evaluations.uchicago.edu/index.php?EvalSearchType=option-number-search&Department=&CourseDepartment=CHEM&CourseNumber=26700&InstructorLastName=&advancedSearch=SEARCH'
# # browser.get(url3)
# url4 = 'https://evaluations.uchicago.edu/evaluation.php?id=54366'

# def get_driver():
#     return browser

def authenticate():
# Opens a request session object, which stores cookies within the session
    with requests.Session() as c:

        # URLs needed to establish and submit login information
        url = 'https://evaluations.uchicago.edu/'
        url2 = "https://shibboleth2.uchicago.edu/idp/profile/SAML2/Redirect/SSO?execution=e1s1"
        url3 = "https://evaluations.uchicago.edu/Shibboleth.sso/SAML2/POST"


        # Your username and password
        USERNAME = input("Please enter your CNET ID: ")
        PASSWORD = getpass('Please enter your my.UChicago password here: ')

        # Go to first URL, which will redirect to log in page
        c.get(url)

        # Store form parameters in dictionary
        login_data = {"j_username":USERNAME, "j_password":PASSWORD, "_eventId_proceed":""}

        # Post (submit) user information and log in
        p = c.post(url2, data=login_data)

        # This locates and gets the encrypted login value of user/pass combo on an intermediary page
        soup = bs4.BeautifulSoup(p.text, 'html5lib')
        encrypted_tag = soup.find(attrs={"name":"SAMLResponse"})
        login_info = encrypted_tag["value"]

        # Store form parameter in dictionary
        log_data = {"SAMLResponse": login_info}

        # Post (submit) the encrypted information
        p = c.post(url3, log_data)

        return c



def get_soup(requester, url):
    # browser.get(url)
    # html = browser.page_source
    soup = bs4.BeautifulSoup(requester.get(url).text.encode('iso-8859-1'), 'html5lib')
    return soup



def is_absolute_url(url):
    '''
    Is url an absolute URL?
    '''
    if url == "":
        return False
    return urllib.parse.urlparse(url).netloc != ""



def convert_if_relative_url(current_url, new_url):
    '''
    Attempt to determine whether new_url is a relative URL and if so,
    use current_url to determine the path and create a new absolute
    URL.  Will add the protocol, if that is all that is missing.

    Inputs:
        current_url: absolute URL
        new_url: 

    Outputs:
        new absolute URL or None, if cannot determine that
        new_url is a relative URL.

    Examples:
        convert_if_relative_url("http://cs.uchicago.edu", "pa/pa1.html") yields 
            'http://cs.uchicago.edu/pa/pa.html'

        convert_if_relative_url("http://cs.uchicago.edu", "foo.edu/pa.html") yields
            'http://foo.edu/pa.html'
    '''
    if new_url == "" or not is_absolute_url(current_url):
        return None

    if is_absolute_url(new_url):
        return new_url

    parsed_url = urllib.parse.urlparse(new_url)
    path_parts = parsed_url.path.split("/")

    if len(path_parts) == 0:
        return None

    ext = path_parts[0][-4:]
    if ext in [".edu", ".org", ".com", ".net"]:
        return "http://" + new_url
    elif new_url[:3] == "www":
        return "http://" + new_path
    else:
        return urllib.parse.urljoin(current_url, new_url)


        
# def quit():
#     browser.quit()