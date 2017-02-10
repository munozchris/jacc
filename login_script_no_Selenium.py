import urllib.request
import urllib.parse
from getpass import getpass
from time import sleep
from requests.exceptions import HTTPError

#Subclass of HTTPRedirectHandler. Does not do much, but is very
#verbose. prints out all the redirects. Compaire with what you see
#from looking at your browsers redirects (using live HTTP Headers or similar)
class ShibRedirectHandler (urllib.request.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        print (req)
        print (fp.geturl())
        print (code)
        print (msg)
        print (headers)
        # without this return (passing parameters onto baseclass) 
        # redirect following will not happen automatically for you.
        return urllib.request.HTTPRedirectHandler.http_error_302(self,
                                                          req,
                                                          fp,
                                                          code,
                                                          msg,
                                                          headers)



for x in range(0, 20):  # try 4 times
  try:
    cookieprocessor = urllib.request.HTTPCookieProcessor()
    opener = urllib.request.build_opener(ShibRedirectHandler, cookieprocessor)

    #Edit: should be the URL of the site/page you want to load that is protected with Shibboleth
    (opener.open("https://evaluations.uchicago.edu/index.php?EvalSearchType=option-number-search&Department=&CourseDepartment=AKKD&CourseNumber=10102&InstructorLastName=&advancedSearch=SEARCH").read())

    print("Made it past 'opener.open of code'")

    #Inspect the page source of the Shibboleth login form; find the input names for the username
    #and password, and edit according to the dictionary keys here to match your input names
    un = input("Please enter your CNETID here: ")
    pw = getpass('Please enter your my.UChicago password here: ')
    loginData = urllib.parse.urlencode({'username':un, 'password':pw})
    bLoginData = loginData.encode('ascii')

    #By looking at the source of your Shib login form, find the URL the form action posts back to
    #hard code this URL in the mock URL presented below.
    #Make sure you include the URL, port number and path
    response = opener.open("https://shibboleth2.uchicago.edu/idp/profile/SAML2/Redirect/SSO?execution=e1s1", bLoginData)
    # response = opener.open("https://shibboleth2.uchicago.edu/idp/profile/SAML2/Redirect/SSO;jsessionid=qn4lxiwm9yyk1imidv8nmdk7?execution=e1s1", bLoginData)
    # response = opener.open("https://shibboleth2.uchicago.edu/idp/profile/SAML2/Redirect/SSO", bLoginData)
    #See what you got.
    print (response.read())

    print(opener.open("https://evaluations.uchicago.edu/index.php?EvalSearchType=option-number-search&Department=&CourseDepartment=AKKD&CourseNumber=10102&InstructorLastName=&advancedSearch=SEARCH").read())
    
    str_error = None

  except HTTPError as str_error:
      pass

  if str_error:
      sleep(2)  # wait for 2 seconds before trying to fetch the data again
  else:
      break