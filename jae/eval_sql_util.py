# Auxiliary function to filter out irrelevant evaluations by year 
# Tag finder code copied from Jae's code

from selenium import webdriver  
import bs4
from login_save import get_auth_driver
import urllib.parse
import re
    
driver = webdriver.Chrome("/usr/local/bin/chromedriver")
    
threshold_year = 2011
url2 = 'https://evaluations.uchicago.edu/index.php?EvalSearchType=option-number-search&Department=&CourseDepartment=AKKD&CourseNumber=10102&InstructorLastName=&advancedSearch=SEARCH'
browser = get_auth_driver(url2)

url3 = 'https://evaluations.uchicago.edu/index.php?EvalSearchType=option-number-search&Department=&CourseDepartment=CHEM&CourseNumber=26700&InstructorLastName=&advancedSearch=SEARCH'
# browser.get(url3)
url4 = 'https://evaluations.uchicago.edu/evaluation.php?id=54366'

def get_driver():
    return browser


def get_soup(url):
    browser.get(url)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, "lxml")
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


def get_eval_links(soup, threshold_year = 2011):
    table = soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="evalSearchResults")
    rows = table.findAll(lambda tag: tag.name=='tr')

    # note: it's find and findAll 
    links = []
    for row in rows[1:]:
        quarter = row.contents[7].text
        year = int(re.search(r'\d{4}', quarter).group())
        year = int(re.search(r'\d{4}', quarter).group())
        if year > threshold_year:
            links.append(row.td.a['href'])

    abs_urls = []
    for link in links:
        abs_link = convert_if_relative_url(url2, link)
        abs_urls.append(abs_link)

    return abs_urls


def quit():
    browser.quit()