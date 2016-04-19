import sys, os, re, requests, urllib
from lxml.html import fromstring

GALLERY_OVERVIEW_URL = "http://www.arto.com/section/user/profile/gallery/?id=%d"
GALLERY_URL = "http://www.arto.com/section/user/profile/gallery/?id=%d&category=%d&ContentList_ActivePage=%d"

def get_galleries(user_id, root, session):
    req = session.get(GALLERY_OVERVIEW_URL % user_id)
    dom = fromstring(req.content)
    folder = root + "images/"
    os.makedirs(folder, exist_ok=True)
    fp = open(folder + "overview.html", 'wb')
    fp.write(req.content)
    fp.close()
  
    # no classes or ids on the tags. Matching on href #yolo
    for elm in dom.xpath(".//a[starts-with(@href,'/section/user/profile/gallery/?id=%d&category=')]" % user_id):
        href = elm.get('href')
        gal_id = int(href.split("=")[-1])

        if gal_id < 0:
            continue

        if elm.find('img') is not None:
            continue

        yield gal_id, elm.text
        

def scrape_gallery(gallery_id, user_id, root, session):
    page_counter = 1
    image_counter = 1
    should_continue = True

    while (should_continue):
        # scrape overview page(s)
        print("     - page %d" % page_counter)

        req = session.get(GALLERY_URL % (user_id, gallery_id, page_counter))
        dom = fromstring(req.content)
        folder = root + "images/" + str(gallery_id) + "/"
        os.makedirs(folder, exist_ok=True)
        fp = open(folder + "gallery-page%d.html" % page_counter, 'wb')
        fp.write(req.content)
        fp.close()

        img_elements = dom.xpath(".//img[contains(@src,'/data/user/gallery')]")
        for img_elm in img_elements:
            src = img_elm.get('src')

            print("       - image %d" % image_counter)
            img_data = session.get(src.replace('thumbs', 'images'))
            image_fp = open(folder + str(image_counter) + ".jpg", 'wb')
            image_fp.write(img_data.content)
            image_fp.close()
            
            image_counter += 1
            
        e = dom.xpath('.//a[text()="Næste"]')        
        page_counter += 1
        
        if not e:
            should_continue = False
    


def scrape_images(user_id, root, session):
    print(" - images")
    for gallery_id, gallery_name in get_galleries(user_id, root, session):

        print("   - gallery: " + gallery_name)
        scrape_gallery(gallery_id, user_id, root, session)
