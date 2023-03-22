#!/bin/bash
mkdir ../../Figures
mkdir server/output 
python3 sele.py 
python3 label.py 
python3 -W ignore countRequests.py 
python3 countTags.py