import requests
from requests.auth import HTTPBasicAuth
import bs4


# Opens a request session object, which stores cookies within the session
with requests.Session() as c:

    # URLs needed to establish and submit login information
    url = 'https://evaluations.uchicago.edu/'
    url2 = "https://shibboleth2.uchicago.edu/idp/profile/SAML2/Redirect/SSO?execution=e1s1"
    url3 = "https://evaluations.uchicago.edu/Shibboleth.sso/SAML2/POST"


    # Your username and password
    USERNAME = ""
    PASSWORD = ""

    # Go to first URL, which will redirect to log in page
    c.get(url)

    # Store form parameters in dictionary
    login_data = {"j_username":USERNAME, "j_password":PASSWORD, "_eventId_proceed":""}

    # Post (submit) user information and log in
    p = c.post(url2, data=login_data)

    # This is a locates and gets the encrypted login value of user/pass combo on an intermediary page
    soup = bs4.BeautifulSoup(p.text, "lxml")
    encrypted_tag = soup.find(attrs={"name":"SAMLResponse"})
    login_info = encrypted_tag["value"]

    # Store form parameter in dictionary
    log_data = {"SAMLResponse": login_info}

    # Post (submit) the encrypted information
    p = c.post(url3, log_data)

    # test links that show login successful
    # NOTE - I imagine this is how you guys will for loop through all the eval links
    # using c.get(eval_link) on each link and calling the scraping code/commiting to database
    url4 = "https://evaluations.uchicago.edu/index.php?EvalSearchType=option-number-search&Department=&CourseDepartment=ARTH&CourseNumber=10100&InstructorLastName=&advancedSearch=SEARCH"
    url5 = "https://evaluations.uchicago.edu/index.php?EvalSearchType=option-number-search&Department=&CourseDepartment=CMST&CourseNumber=10100&InstructorLastName=&advancedSearch=SEARCH"
    g = c.get(url4)
    print(g.text)
    g = c.get(url5)
    print(g.text)