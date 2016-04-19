import os
from slugify import slugify

def make_user_folder(profile_id, username):
    # we arrange the users in folders of 10000
    remainder = profile_id % 100000
    subfolder = profile_id - remainder

    sanitized_name = slugify(username)
    
    folder = "out/%d/%d-%s/" % (subfolder, profile_id, sanitized_name)

    os.makedirs(folder, exist_ok=True)
    
    return folder
