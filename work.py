import os,sys
import progressbar, requests
from user import get_everything

bar = progressbar.ProgressBar(max_value=5000, redirect_stdout=True)

work_filename = sys.argv[1].split("/")[-1]
out = open("log-%s-%s.txt" % (str(os.getpid()), work_filename), "w")


filename = sys.argv[1]

os.rename(filename, filename+".working")
with open(filename+".working", 'r') as fp:
    s = requests.Session()
    
    for line in bar(fp):
        aid = int(line.rstrip())
        try:
            get_everything(aid, s)
            out.write("%d;succeeded\n" % aid)
        except:
            out.write("%d;failed\n" % aid)

os.rename(filename+".working", filename+".done")
out.close()
