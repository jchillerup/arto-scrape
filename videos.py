import sys, os, re, requests, urllib, demjson
from lxml.html import fromstring
from util import download_file

VIDEO_OVERVIEW_URL = "http://www.arto.com/section/user/profile/gallery/?id=%d&category=-1&ContentList_ActivePage=%d"
VIDEO_URL = ""

    
def dump_video(video_url, video_counter, root, session):
    vreq = session.get(video_url)
    vfp = open(root + "video%d.html" % video_counter, "wb")
    vfp.write(vreq.content)
    vfp.close()

    dom = fromstring(vreq.content)
    
    player_div = dom.find(".//div[@id='UserVideoPlayerObjectDiv']")
    obj = demjson.decode(player_div.getnext().text[58:-11])
    file_url = obj['modes'][1]['config']['file']

    download_file(session, file_url, root+"video%d.flv"%video_counter)

def scrape_videos(user_id, root, session):
    print(" - videos")

    page_counter = 1
    video_counter = 1
    should_continue = True
    
    while(should_continue):
        print("   - page %d" % page_counter)
        
        req = session.get(VIDEO_OVERVIEW_URL % (user_id, page_counter))
        dom = fromstring(req.content)
        folder = root + "videos/"
        os.makedirs(folder, exist_ok=True)
        fp = open(folder + "gallery-page%d.html" % page_counter, 'wb')
        fp.write(req.content)
        fp.close()

        # we're doing a depth first search
        thumbs = dom.xpath(".//div[@class='galleryThumb']")
        for thumb in thumbs:
            print("       - video %d" % video_counter)
            video_url = "http://www.arto.com" + thumb.getchildren()[0].get('href')
            video_thumb = thumb.getchildren()[0][0].get('src')

            download_file(session, video_thumb, folder+"video%d.jpg"%video_counter)

            dump_video(video_url, video_counter, folder, session)
            
            video_counter += 1

        e = dom.xpath('.//a[text()="Næste"]')        
        page_counter += 1
        
        if not e:
            should_continue = False
        
        
