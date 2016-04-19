import sys, os, re, requests, urllib
from lxml.html import fromstring

FRIENDS_URL = "http://www.arto.com/section/user/profile/friends/default.aspx?id=%d&FriendRepeater_ActivePage=%d"

def scrape_friends(user_id, root, session):
    print(" - friends")
    
    page_counter = 1
    should_continue = True

    folder = root+"friends/"
    os.makedirs(folder, exist_ok=True)
    
    while (should_continue):
        print("   - page %d" % page_counter)
        
        req = session.get(FRIENDS_URL % (user_id, page_counter))
        dom = fromstring(req.content)

        fp = open(folder+"page%d.html"%page_counter, 'wb')
        fp.write(req.content)
        fp.close()

        e = dom.xpath('.//a[text()="Næste"]')
        page_counter += 1
    
        if not e:
            should_continue = False
