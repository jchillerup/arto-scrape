import sys, os, re, requests, urllib
from lxml.html import fromstring
from user import make_user_folder

GUESTBOOK_URL = "http://www.arto.com/section/user/profile/guestbook/?id=%d&GuestbookRepeater_ActivePage=%d"

def scrape_guestbook(profile_id, root):
    page_counter = 1
    should_continue = True

    print(" - guestbook")
    
    while(should_continue):
        
        req = requests.get(GUESTBOOK_URL % (profile_id, page_counter))
        dom = fromstring(req.content)
        folder = root+"guestbook/"
        os.makedirs(folder, exist_ok=True)
        fp = open(folder + "page-%d.html" % page_counter, 'wb')
        fp.write(req.content)
        fp.close()

        print("   - page %d" % page_counter)
        
        e = dom.xpath('.//a[text()="Næste"]')        
        page_counter += 1
        
        if not e:
            should_continue = False


if __name__=='__main__':
    scrape_guestbook(5328127, "test/")
