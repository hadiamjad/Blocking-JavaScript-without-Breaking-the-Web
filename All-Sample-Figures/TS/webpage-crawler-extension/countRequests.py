import tldextract
import math
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import traceback
from urllib.parse import urlparse
import os

def checkResExist(df, request_id):
    return request_id in df["request_id"].values

def getInitiatorURL(stack):
    if len(stack["callFrames"]) != 0:
        return stack["callFrames"][0]["url"]
    else:
        return getInitiatorURL(stack["parent"])

def extractDigits(lst):
    return list(map(lambda el: [el], lst))

def main():
    df1 = pd.DataFrame(extractDigits(os.listdir('../../TS/webpage-crawler-extension/server/output')), columns=['website'])
    tracking = 0
    functional = 0
    for j in df1.index:
        try:
            print('server/output/' + df1["website"][j] + '/label_request.json')
            df = pd.read_json('server/output/' + df1["website"][j] + '/label_request.json') 
            res = pd.read_json('server/output/' + df1["website"][j] + '/responses.json', lines=True)    
            for i in df.index:
                if checkResExist(res, df["request_id"][i]):
                    if (df["easylistflag"][i] == 1 or df["easyprivacylistflag"][i] == 1 or df["ancestorflag"][i] == 1):
                            tracking +=1
                    else:
                            functional +=1
        except:
                pass

    print ("total tracking requests:", tracking, "total functional requests:", functional)
main() 