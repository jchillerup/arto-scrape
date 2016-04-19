import re, sys, os
import requests, urllib
from lxml.html import fromstring
from util import download_file

PROFILE_URL = "http://www.arto.com/section/user/profile/?id=%d"
AVATAR_URL = "http://artoimages.cloud2.artodata.com/data/user/profile/medium/%s/%d.jpg"
PANES_URL = "http://www.arto.com/section/user/profile/widget/profiletext/?widgetUserID=%d"

def get_avatar(profile_id):
    last_four = str(profile_id)[-4:]
    
    url = AVATAR_URL % (last_four, profile_id)

def get_presentation(profile_id, folder, session):
    req = session.get(PANES_URL % profile_id)
    dom = fromstring(req.content)

    panes = dom.xpath(".//td[@class='smallTabItemContent']")
    for pane_number, pane in enumerate(panes):
        print("   - pane %d" % pane_number)
        clickhandler = pane.get('onclick')
        pane_url = re.search("(?P<url>https?://[^\s']+)", clickhandler).group("url")

        download_file(session, pane_url, folder + "presentation%d.html" % pane_number)

    if len(panes) == 0:
        print("   - sole pane")
        iframe = dom.xpath(".//iframe[@id='ProfileTextIFrame']")[0]
        download_file(session, iframe.get('src'), folder+"presentation.html")
        
def scrape_profile(profile_id, folder, session):
    req = session.get(PROFILE_URL % profile_id)
    dom = fromstring(req.content)

    username = dom.findtext(".//title").replace("Arto - ", "").strip()
    
    ## PROFILE
    print(" - profile")
    fp = open(folder + "profile.html", 'wb')
    fp.write(req.content)
    fp.close()
    
    ## AVATAR
    print (" - avatar")
    avatar_url = re.findall('url\(([^)]+)\)', 
                            dom.find(".//div[@id='photoContainerDiv']").get('style')
                            )[0].split("?")[0]

    urllib.request.urlretrieve(avatar_url, folder + "avatar.jpg")


    print (" - presentation")
    get_presentation(profile_id, folder, session)

    print (" - statistics")
    download_file(session, "http://www.arto.com/section/user/statistics/?id=%d"%profile_id, folder+"statistics.html")
    
if __name__=='__main__':
    s = requests.Session()
    scrape_profile(5777177, "test/", s)
