#!/bin/bash
rm server/output  2>&1 /dev/null
mkdir server/output 
python3 sele.py 
python3 label.py 
python3 -W ignore countRequests.py 
python3 countTags.py