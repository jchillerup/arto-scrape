
def download_file(session, url, destination):
    req = session.get(url)
    fp = open(destination, 'wb')
    fp.write(req.content)
    fp.close()
