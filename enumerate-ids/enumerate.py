import requests
import grequests
import progressbar

URL = "http://www.arto.com/section/user/profile/?id=%d"
out = open('users.csv', 'a')

counter = 0

blarange = range(4922430, 0, -1)

def handle_response(resp, *args, **kwargs):        
    out.write("%s;%s\n" % (resp.url.split("=")[-1], resp.headers['Content-Length']))

def exception_handler(req, exception):
    print(exception)

hooks = dict(response=handle_response)

def get_requests():
    for i in blarange:
        yield grequests.get(URL % i, hooks=hooks, allow_redirects=False)

bar = progressbar.ProgressBar(max_value=len(blarange))

for response in bar(grequests.imap(get_requests(), size=50, exception_handler=exception_handler)):
    out.write("%s;%s\n" % (response.url.split("=")[-1], response.headers['Content-Length']))

out.close()
