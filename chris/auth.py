import requests
from requests.auth import HTTPBasicAuth
import bs4



with requests.Session() as c:
    url = 'https://evaluations.uchicago.edu/'
    url2 = "https://shibboleth2.uchicago.edu/idp/profile/SAML2/Redirect/SSO?execution=e1s1"
    url3 = "https://evaluations.uchicago.edu/Shibboleth.sso/SAML2/POST"
    USERNAME = ""
    PASSWORD = ""
    c.get(url)
    token = c.cookies["JSESSIONID"]
    #print('this is a token', token)
    login_data = {"j_username":USERNAME, "j_password":PASSWORD, "_eventId_proceed":""}
    p = c.post(url2, data=login_data)
    soup = bs4.BeautifulSoup(p.text, "lxml")
    inputTag = soup.find(attrs={"name":"SAMLResponse"})
    input_tag = inputTag["value"]
    print(input_tag)
    l_data = {"SAMLResponse": input_tag}
    p = c.post(url3, l_data)
    url4 = "https://evaluations.uchicago.edu/index.php?EvalSearchType=option-number-search&Department=&CourseDepartment=ARTH&CourseNumber=10100&InstructorLastName=&advancedSearch=SEARCH"
    url5 = "https://evaluations.uchicago.edu/index.php?EvalSearchType=option-number-search&Department=&CourseDepartment=CMST&CourseNumber=10100&InstructorLastName=&advancedSearch=SEARCH"
    g = c.get(url4)
    print(g.text)
    g = c.get(url5)
    print(g.text)

    soup = bs4.BeautifulSoup(p.text, "lxml")

    total_enrollment = soup.find(id="page-title")

    #print(total_enrollment)