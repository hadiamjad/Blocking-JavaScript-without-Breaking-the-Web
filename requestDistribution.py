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

def countDistribution(experiment):
    df1 = pd.DataFrame(extractDigits(os.listdir(''+experiment+'/webpage-crawler-extension/server/output')), columns=['website'])
    fold = ''+experiment+'/webpage-crawler-extension/'
    website = {}
    for j in df1.index:
        if df1["website"][j] not in website:
            website[df1["website"][j]] = [0,0,0,0]
        # try:
        df = pd.read_json(fold + 'server/output/' + df1["website"][j] + '/label_request.json') 
        res = pd.read_json(fold +'server/output/' + df1["website"][j] + '/responses.json', lines=True)    
        for i in df.index:
            if checkResExist(res, df["request_id"][i]):
                if (df["easylistflag"][i] == 1 or df["easyprivacylistflag"][i] == 1 or df["ancestorflag"][i] == 1):
                    website[df1["website"][j]][0] +=1
                else:
                    website[df1["website"][j]][1] +=1
        df = pd.read_json('Control/webpage-crawler-extension/server/output/' + df1["website"][j] + '/label_request.json')   
        for i in df.index:
            if (df["easylistflag"][i] == 1 or df["easyprivacylistflag"][i] == 1 or df["ancestorflag"][i] == 1):
                website[df1["website"][j]][2] +=1
            else:
                website[df1["website"][j]][3] +=1
        # except:
        #         pass
    data = {
    'Website': list(website.keys()),
    'Tracking': [(item[2]-item[0])*100/item[2] for item in website.values()],
    'Functional': [(item[3]-item[1])*100/item[3] for item in website.values()]
    }

    # create a pandas dataframe from the dictionary
    df = pd.DataFrame(data)
    # Use the melt function to unpivot the dataframe
    df = pd.melt(df, id_vars=['Website'], var_name='Function', value_name='Value')
    # plotting the bar plot
    colors = ['#E11916', '#3FD72D']
    sns.displot(df, x="Value", hue="Function", multiple="dodge",palette = colors, bins=10)   
    plt.show()
    plt.savefig('Figures/DistributionPlot.pdf')

def main():
    countDistribution(sys.argv[1])
main()