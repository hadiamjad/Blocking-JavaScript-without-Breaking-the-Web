import tldextract
import math
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import traceback
from urllib.parse import urlparse
import os

# Description: extract domain from given url
# input: url = url for which domain is needed
# return: domain
def getDomain(url):
    ext = tldextract.extract(url)
    return ext.domain + "." + ext.suffix


# Description: check if its thirparty request
# input: url = url
# input: top_level_url = top_level_url
# return: returns True if its thirdparty request otherwise false
def isThirdPartyReq(url, top_level_url):
    d_url = getDomain(url)
    d_top_level_url = getDomain(top_level_url)
    if d_url == d_top_level_url:
        return False
    else:
        return True

def getInitiatorURL(stack):
    if len(stack["callFrames"]) != 0:
        return stack["callFrames"][0]["url"]
    else:
        return getInitiatorURL(stack["parent"])

def extractDigits(lst):
    return list(map(lambda el: [el], lst))

def main():
    df1 = pd.DataFrame(extractDigits(os.listdir('/home/student/TrackerSift/ASE-22/Control/webpage-crawler-extension/server/output')), columns=['website'])
    script = {}
    for j in df1.index:
        try:
            print('server/output/' + df1["website"][j] + '/label_request.json')
            df = pd.read_json('server/output/' + df1["website"][j] + '/label_request.json')     
            for i in df.index:
                # try:
                    if df["call_stack"][i]["type"] == "script":
                        if getInitiatorURL(df["call_stack"][i]["stack"]) not in script.keys():
                            script[getInitiatorURL(df["call_stack"][i]["stack"])]=[0, 0, []]
                        if df["top_level_url"][i] not in script[getInitiatorURL(df["call_stack"][i]["stack"])][2]:
                            script[getInitiatorURL(df["call_stack"][i]["stack"])][2].append(df["top_level_url"][i])
                        if (df["easylistflag"][i] == 1 or df["easyprivacylistflag"][i] == 1 or df["ancestorflag"][i] == 1):
                            script[getInitiatorURL(df["call_stack"][i]["stack"])][0] +=1
                        else:
                            script[getInitiatorURL(df["call_stack"][i]["stack"])][1] +=1
        except:
                pass

    thirdparty = 0
    firstparty = 0
    for key in script:
        # if script[key][1] == 0:
            for item in script[key][2]:
                if getDomain(key) == getDomain(item):
                    firstparty +=1
                else:
                    thirdparty +=1

    print (firstparty, thirdparty, len(script))
main() 