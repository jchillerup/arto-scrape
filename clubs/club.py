import requests
from lxml.html import fromstring
from util import make_payload_from_dom
OVERVIEW_URL = "http://www.arto.com/section/club/ClubInfo.aspx?TabPage=1&id=%d"

class Club():
    club_id = None
    session = None

    name = None
    
    def __init__(self, club_id, session):
        self.club_id = club_id
        self.session = session

    def attempt_join(self):
        print("[-] Attempting to join club")

        r = self.session.get('http://www.arto.com/section/club/ClubInfo.aspx?id=%d&TabPage=1&TabContent=ApplyClub' % self.club_id)
        dom = fromstring(r.content)

        self.name = dom.xpath('.//span[@id="pageHeaderText"]')[0].text.strip()
        
        payload = make_payload_from_dom(dom)

        # r2 = self.session.post('')
        payload['ctl00$ctl00$ctl00$Main$Main$Main$ctl00$ctl00$AcceptCheckBox'] = "on"

        r2 = self.session.post('http://www.arto.com/section/club/ClubInfo.aspx?id=%d&TabPage=1&TabContent=ApplyClub' % self.club_id, data=payload)

        print("[-] Joined group: %s" % self.name)

    def get_overview(self):
        r = self.session.get(OVERVIEW_URL % self.club_id)
        
        # get all presentation panes from $("#FrontMenuProfileTabRepeater")
        # $(".smallTabItemContentSelected") og $(".smallTabItemContent")

        # get onclicks
        
    def get_all(self):
        self.attempt_join()
        pass
        #overview = ClubOverview()

     
