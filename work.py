import os,sys
import progressbar, requests
from user import get_everything

bar = progressbar.ProgressBar(max_value=5000, redirect_stdout=True)

out = open("log-"+str(os.getpid()) + ".txt", "w")

with open(sys.argv[1], 'r') as fp:
    s = requests.Session()
    
    for line in bar(fp):
        aid = int(line.rstrip())
        try:
            get_everything(aid, s)
            out.write("%d;succeeded\n" % aid)
        except:
            out.write("%d;failed\n" % aid)

out.close()
