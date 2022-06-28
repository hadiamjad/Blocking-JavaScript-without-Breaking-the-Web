# This file contains the logic for handling information sharing i.e. cookie key value pair in headers and urls
import json

# getting the associated cookies with the request id
"""
request_id = ['dc=was1; tuuid=8355a7eb-f3f1-532f-bfb3-c90fddbef41e; ut=Yg09EQAD_3D4aehR4WmgY-sH2xPg1BHtDBH8KA==; ss=1', ..]
"""


def getReqCookie(request_id, page_url):
    lst = []
    with open(page_url + "requestInfo.json") as file:
        for line in file:
            dataset = json.loads(line)
            if dataset["request_id"] == request_id:
                if "cookie" in dataset["headers"].keys():
                    lst.append(dataset["headers"]["cookie"])
    return lst


# Function checks if storage key-value is shared in url or not
def IsInfoShared(storage_dic, url):
    for key in storage_dic:
        for item in storage_dic[key]:
            if item in url:
                return key

    return None
