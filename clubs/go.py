import requests
from lxml.html import fromstring
from club import Club
from util import make_payload_from_dom

USERNAME = "JCArkiverer"
PASSWORD = "JCArkiverer"

def get_arto_session():
    print("[-] Logging into Arto")
    s = requests.Session()

    s.headers.update({
        'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
    })
    
    r = s.get('http://www.arto.com/')
    # get the hidden fields

    dom = fromstring(r.content)
    payload = make_payload_from_dom(dom)
    payload['ctl00$ctl00$Main$SiteTopBar$ArtoLoginBox$UsernameTextbox'] = USERNAME
    payload['ctl00$ctl00$Main$SiteTopBar$ArtoLoginBox$PasswordTextbox'] = PASSWORD

    login_request = s.post('http://www.arto.com/section/frontpage/', data=payload)

    r = s.get('http://www.arto.com/section/user/activity/')
        
    return s

if __name__ == '__main__':
    s = get_arto_session()
    
    # støt brysterne
    c = Club(50111, s)
    c.attempt_join()

    c = Club(13165, s)
    c.attempt_join() 

    c = Club(54029, s)
    c.attempt_join()
