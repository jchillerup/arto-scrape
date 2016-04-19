#!/bin/bash
echo $(date +%s),$(du -s /data/jc/arto/arto-scrape/out/|cut -f1) >> /data/jc/arto/arto-scrape/log-dump-size.csv
