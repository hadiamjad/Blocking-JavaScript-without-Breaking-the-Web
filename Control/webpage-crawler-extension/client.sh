#!/bin/bash
rm  ../../Figures 2>&1 /dev/null
mkdir ../../Figures
rm server/output  2>&1 /dev/null
mkdir server/output
python3 sele.py
python3 label.py
python3 SBFL.py
python3 -W ignore countRequests.py
