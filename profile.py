import re, sys, os
import requests, urllib
from lxml.html import fromstring
from util import make_user_folder

PROFILE_URL = "http://www.arto.com/section/user/profile/?id=%d"
AVATAR_URL = "http://artoimages.cloud2.artodata.com/data/user/profile/medium/%s/%d.jpg"

def get_avatar(profile_id):
    last_four = str(profile_id)[-4:]
    
    url = AVATAR_URL % (last_four, profile_id)

def scrape_profile(profile_id):
    req = requests.get(PROFILE_URL % profile_id)
    dom = fromstring(req.content)

    username = dom.findtext(".//title").replace("Arto - ", "").strip()
    folder = make_user_folder(profile_id, username)

    print(":: Dumping %s to %s" % (username, folder))

    ## PROFILE
    print(" - profile")
    fp = open(folder + "profile.html", 'wb')
    fp.write(req.content)
    fp.close()
    
    ## AVATAR
    avatar_url = re.findall('url\(([^)]+)\)', 
                            dom.find(".//div[@id='photoContainerDiv']").get('style')
                            )[0].split("?")[0]

    urllib.request.urlretrieve(avatar_url, folder + "avatar.jpg")
    print (" - avatar")

if __name__=='__main__':
    scrape_profile(5777177)
