import gzip
import progressbar
import subprocess

fp = gzip.open('user-content-lengths.csv.gz', 'rb')
out = open('users-active.txt', 'w')

skipped = 0

bar = progressbar.ProgressBar(max_value=7999999)

for line in bar(fp):
    id_, size_ = line.decode().rstrip().split(";")

    if int(size_) <= 510:
        skipped +=1
    else:
        out.write("%s\n" % id_)


print("Skipped %d" % skipped)
    
