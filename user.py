import os
from slugify import slugify
import requests

from profile import scrape_profile
from guestbook import scrape_guestbook


def make_user_folder(profile_id):
    # we arrange the users in folders of 10000
    remainder = profile_id % 100000
    subfolder = profile_id - remainder

    #sanitized_name = slugify(username)
    
    folder = "out/%d/%d/" % (subfolder, profile_id)

    os.makedirs(folder, exist_ok=True)
    
    return folder


def get_everything(user_id):
    print(":: %d" % user_id)
    folder = make_user_folder(user_id)

    s = requests.Session()
    scrape_profile(user_id, folder, s)
    scrape_guestbook(user_id, folder, s)
    

if __name__=='__main__':
    get_everything(5328127)
    
