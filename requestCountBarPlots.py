import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import sys
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

def countRequests(experiment):
    df1 = pd.DataFrame(extractDigits(os.listdir(''+experiment+'/webpage-crawler-extension/server/output')), columns=['website'])
    fold = ''+experiment+'/webpage-crawler-extension/'
    tracking = 0
    functional = 0
    for j in df1.index:
        try:
            df = pd.read_json(fold + 'server/output/' + df1["website"][j] + '/label_request.json') 
            res = pd.read_json(fold +'server/output/' + df1["website"][j] + '/responses.json', lines=True)    
            for i in df.index:
                if checkResExist(res, df["request_id"][i]):
                    if (df["easylistflag"][i] == 1 or df["easyprivacylistflag"][i] == 1 or df["ancestorflag"][i] == 1):
                            tracking +=1
                    else:
                            functional +=1
        except:
                pass

    return tracking,functional

def countDistribution(experiment):
    df1 = pd.DataFrame(extractDigits(os.listdir(''+experiment+'/webpage-crawler-extension/server/output')), columns=['website'])
    fold = ''+experiment+'/webpage-crawler-extension/'
    tracking = 0
    functional = 0
    website = {}
    for j in df1.index:
        if df1["website"][j] not in website:
            website[df1["website"][j]] = [(0,0), (0,0)]
        try:
            df = pd.read_json(fold + 'server/output/' + df1["website"][j] + '/label_request.json') 
            res = pd.read_json(fold +'server/output/' + df1["website"][j] + '/responses.json', lines=True)    
            for i in df.index:
                if checkResExist(res, df["request_id"][i]):
                    if (df["easylistflag"][i] == 1 or df["easyprivacylistflag"][i] == 1 or df["ancestorflag"][i] == 1):
                        website[df1["website"][j]][0][0] +=1
                    else:
                        website[df1["website"][j]][0][1] +=1
            df = pd.read_json('ALL/webpage-crawler-extension/server/output/' + df1["website"][j] + '/label_request.json')   
            for i in df.index:
                if (df["easylistflag"][i] == 1 or df["easyprivacylistflag"][i] == 1 or df["ancestorflag"][i] == 1):
                    website[df1["website"][j]][1][0] +=1
                else:
                    website[df1["website"][j]][1][0] +=1
        except:
                pass

    return tracking,functional

def main():
    if sys.argv[2] != "None":
        data = {
            "Control": countRequests("Control"),
            sys.argv[1]: countRequests(sys.argv[1]),
            sys.argv[2]: countRequests(sys.argv[2])
            }
    else:
         data = {
            "Control": countRequests("Control"),
            sys.argv[1]: countRequests(sys.argv[1])
            }
    # Create DataFrame     
    df = pd.DataFrame(data.items(), columns=['experiment', 'tracking, functional'])
    df[['tracking', 'functional']] = pd.DataFrame(df['tracking, functional'].tolist(), index=df.index)
    df = df[['experiment', 'tracking', 'functional']]
    
    # Plot
    colors = ['#E11916', '#3FD72D']
    ax = df.plot(kind='bar', x='experiment', y=['tracking', 'functional'], color=colors, rot=0)
    ax.set_xlabel('Experiment')
    ax.set_ylabel('Value')
    plt.show()
    plt.savefig('Figures/BarPlot.pdf')
main()