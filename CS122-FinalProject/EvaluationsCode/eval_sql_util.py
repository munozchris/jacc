# eval_sql_util.py
# Auxiliary functions for "eval_sql.py"
# Tag finder code copied from Jae's code


# from selenium import webdriver  
import bs4
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
    ''' 
    Opens a request session object, which stores cookies within the session
    and returns the requests session for use with BeautifulSoup
    Inputs -
        (None)

    Returns - 
        c (requests Object) 
    '''
    
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
        p = c.post(url2, data = login_data)

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
    '''
    Disclaimer: text.encode methodology borrowed directly from pa2
    Returns soup object for HTML scraping

    Inputs - 
        requester (Requests object/authenticated session)
        url (str): absolute eval url
    '''

    # browser.get(url)
    # html = browser.page_source
    soup = bs4.BeautifulSoup(requester.get(url).text.encode('iso-8859-1'), 'html5lib')
    return soup



def is_absolute_url(url):
    '''
    Disclaimer: borrowed directly from pa2
    Checks to see if url is an absolute url

    Inputs - 
        url (str): url to check

    Returns - 
        Boolean
    '''
    
    if url == "":
        return False
    return urllib.parse.urlparse(url).netloc != ""



def convert_if_relative_url(current_url, new_url):
    '''
    Disclaimer: borrowed directly from pa2

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



def parse_eval_table(soup, header_text, TA):
    '''
    Returns the max value for each row in an either a TA_eval or a non-TA eval
    as a dictionary
    or if two ratings have the highest frequency in a table, takes the max to be the 
    last category encountered 
    Helper function for "get_eval_info function"

    Inputs - 
        soup (bs4 object)
        header_text (str)
        TA (boolean): Whether the soup object passed into this function is of 
        the TA_eval type or non-TA_eval type

    Returns - 
        rv (dictionary): highest frequency vote for each category 
    '''
        
    col_tags = soup.find('h2', text=header_text).nextSibling.nextSibling.findAll('th')[1:7]
    row_tags = soup.find('h2', text=header_text).nextSibling.nextSibling.findAll('th')[7:]

    col_text = [x.text for x in col_tags]
    
    if TA:
        row_text = [x.text[:-1] for x in row_tags]
    elif not TA:
        row_text = [x.text for x in row_tags]

    rows = [x.findAll('td') for x in soup.find('h2', text=header_text).nextSibling.nextSibling.findAll('tr', {'class':'gridNA grid'})]
    
    table_greatest = []
    for row_els in rows:
        for i in range(len(row_els)):
            if row_els[i].has_attr('class'):
                table_greatest.append(i)
    rv = {}
    for i in range(len(row_text)):
        rv[row_text[i]] = col_text[table_greatest[i]]

    return rv



def parse_lang_table(soup, header_type, header_text, tr_class, options):
    '''
    Like parse_eval_table but for language tables that are formatted differently
    Return the highest frequency vote for each category or the latest max
    if there are multiple max frequency counts

    Inputs - 
        soup (bs4 object)
        header_type (str): 'h2' or 'h3'
        header_text (str): header text of the table to locate int
        tr_class (str): tr_class text
        options: (int) number of categories (columns)

    Returns - 
        rv (dictionary)
    '''
        
    col_tags = soup.find(header_type, text=header_text).nextSibling.nextSibling.findAll('th')[1:(options + 1)]
    row_tags = soup.find(header_type, text=header_text).nextSibling.nextSibling.findAll('th')[(options + 1):]

    col_text = [x.text for x in col_tags]
    row_text = [x.text for x in row_tags]
    
    rows = [x.findAll('td') for x in soup.find(header_type, 
        text=header_text).nextSibling.nextSibling.findAll('tr', {'class':tr_class})]

    table_greatest = []
    for aspect in rows:
        counts = []
        for i in range(len(aspect)):
            if aspect[i].has_attr('class'):
                counts.append(col_text[i])   
        table_greatest.append(counts)
    
    rv = {}
    for i in range(len(row_text)):
        if len(table_greatest[i]) == 1:
            rv[row_text[i]] = table_greatest[i][0]
        else:
            rv_str = ''
            for val in table_greatest[i]:
                rv_str += val + ' & '
            rv[row_text[i]] = rv_str[:-3]
    
    if len(rv) == 1:
        for key in rv:
            return rv[key]
    
    return rv



def parse_lang_table_wtag(soup, tag, tr_class, options):
    '''
    Another function to process language type eval tables 
    if the table cannot be found using header text easily
    is also a more accessible function
    Has the same functionality as parse_lang_table

    Inputs - 
        soup (bs4 object)
        tag (HTML tag): contains the table_greatest
        tr_class (str): tr_class text
        options (int): number of categories (columns)

    Returns - 
        rv (dictionary)
    '''
    
    col_tags = tag.findAll('th')[1:(options + 1)]
    row_tags = tag.findAll('th')[(options + 1):]

    col_text = [x.text for x in col_tags]
    row_text = [x.text for x in row_tags]
    
    rows = [x.findAll('td') for x in tag.findAll('tr', {'class':tr_class})]

    table_greatest = []
    for aspect in rows:
        counts = []
        for i in range(len(aspect)):
            if aspect[i].has_attr('class'):
                counts.append(col_text[i])   
        table_greatest.append(counts)
    
    rv = {}
    for i in range(len(row_text)):
        if len(table_greatest[i]) == 1:
            rv[row_text[i]] = table_greatest[i][0]
        else:
            rv_str = ''
            for val in table_greatest[i]:
                rv_str += val + ' & '
            rv[row_text[i]] = rv_str[:-3]
    
    if len(rv) == 1:
        for key in rv:
            return rv[key]
    
    return rv



def get_comments_list(soup, header_type, header_text):
    '''
    From a <ul> tag, grabs all the <li> elements and combines
    them into a monster string for easier storage in the SQL table_greatest

    Inputs - 
        soup (bs4 object)
        header_type (str): 'h2' or 'h3'
        header_text (str): header text of the tag you're looking for

    Returns - 
        rv (str)
    '''
    
    remarks = [x.text for x in soup.find(header_type, text=header_text).nextSibling.nextSibling.findAll('li')]
    rv = ""
    for remark in remarks:
        rv += remark + ' '
    return rv[:-1]


def parse_bar_table(soup, header_text):
    '''
    Returns the category (column value) with the highest count from a 
    bar table in an eval as a dictionary

    Inputs - 
        soup (bs4 object)
        header_text (str): bar table header text for easier location

    Returns - 
        rv (dictionary)
    '''

    row_text = [x.text for x in soup.find('h3', text=header_text).nextSibling.nextSibling.findAll('th')]
    col_counts = count_tags = [int(re.search(r'\d+', x.text).group()) for x in soup.find('h3', 
        text=header_text).nextSibling.nextSibling.findAll('td', {'class':'count-totals'})]
    rv = {}
    for i in range(len(row_text)):
        rv[row_text[i]] = col_counts[i]

    return rv
        
