import math
import numpy as np
import pandas as pd
import json
import os


def checkResExist(df, request_id):
    return request_id in df["request_id"].values


def extractDigits(lst):
    return list(map(lambda el: [el], lst))


def main():
    df = pd.DataFrame(
        extractDigits(
            os.listdir(
                "/home/student/TrackerSift/ScriptML/webpage-crawler-extension/server/output"
            )
        ),
        columns=["website"],
    )
    fold = "/home/student/TrackerSift/ScriptML/ASE-22/"
    result = (
        {}
    )  # 'website': control-tracking, control-functional,  script-tracking, script-functional, method-tracking, method-functional
    for i in df.index:
        try:
            # creating dictionary
            if df["website"][i] not in result:
                result[df["website"][i]] = [0, 0, 0, 0, 0, 0]

            # opening request and response file for script
            control_req = pd.read_json(
                "/home/student/TrackerSift/ScriptML/webpage-crawler-extension/server/output/"
                + df["website"][i]
                + "/label_request.json"
            )
            # coutning requests
            seriesObj = control_req.apply(
                lambda x: True
                if x["easylistflag"] == 1
                or x["easyprivacylistflag"] == 1
                or x["ancestorflag"] == 1
                else False,
                axis=1,
            )
            tracking = len(seriesObj[seriesObj == True].index)
            seriesObj = control_req.apply(
                lambda x: True
                if x["easylistflag"] == 0
                and x["easyprivacylistflag"] == 0
                and x["ancestorflag"] == 0
                else False,
                axis=1,
            )
            functional = len(seriesObj[seriesObj == True].index)
            # updating dictionary
            result[df["website"][i]][0] = tracking
            result[df["website"][i]][1] = functional

            # opening request and response file for
            print(
                fold
                + "MixScripts/webpage-crawler-extension/server/output/"
                + df["website"][i]
                + "/label_request.json"
            )
            script_req = pd.read_json(
                fold
                + "MixScripts/webpage-crawler-extension/server/output/"
                + df["website"][i]
                + "/label_request.json"
            )
            script_res = pd.read_json(
                fold
                + "MixScripts/webpage-crawler-extension/server/output/"
                + df["website"][i]
                + "/responses.json",
                lines=True,
            )
            # see if request is block
            script_req["not-block"] = script_req.apply(
                lambda row: checkResExist(script_res, row.request_id), axis=1
            )
            # counting request numbers
            seriesObj = script_req.apply(
                lambda x: True
                if x["easylistflag"] == 1
                or x["easyprivacylistflag"] == 1
                or x["ancestorflag"] == 1
                and x["not-block"] == True
                else False,
                axis=1,
            )
            tracking = len(seriesObj[seriesObj == True].index)
            seriesObj = script_req.apply(
                lambda x: True
                if x["easylistflag"] == 0
                and x["easyprivacylistflag"] == 0
                and x["ancestorflag"] == 0
                and x["not-block"] == True
                else False,
                axis=1,
            )
            functional = len(seriesObj[seriesObj == True].index)
            # updating dictionary
            result[df["website"][i]][2] = tracking
            result[df["website"][i]][3] = functional

            # opening request and response file for method
            method_req = pd.read_json(
                fold
                + "MixMethods/webpage-crawler-extension/server/output/"
                + df["website"][i]
                + "/label_request.json"
            )
            method_res = pd.read_json(
                fold
                + "MixMethods/webpage-crawler-extension/server/output/"
                + df["website"][i]
                + "/responses.json",
                lines=True,
            )
            # see if request is block
            method_req["not-block"] = method_req.apply(
                lambda row: checkResExist(method_res, row.request_id), axis=1
            )
            # counting request numbers
            seriesObj = method_req.apply(
                lambda x: True
                if x["easylistflag"] == 1
                or x["easyprivacylistflag"] == 1
                or x["ancestorflag"] == 1
                and x["not-block"] == True
                else False,
                axis=1,
            )
            tracking = len(seriesObj[seriesObj == True].index)
            seriesObj = method_req.apply(
                lambda x: True
                if x["easylistflag"] == 0
                and x["easyprivacylistflag"] == 0
                and x["ancestorflag"] == 0
                and x["not-block"] == True
                else False,
                axis=1,
            )
            functional = len(seriesObj[seriesObj == True].index)
            # updating dictionary
            result[df["website"][i]][4] = tracking
            result[df["website"][i]][5] = functional

            print(df["website"][i])
        except:
            print("fail")
            result[df["website"][i]][0] = 0
            result[df["website"][i]][1] = 0
            result[df["website"][i]][2] = 0
            result[df["website"][i]][3] = 0
            result[df["website"][i]][4] = 0
            result[df["website"][i]][5] = 0

    # saving in excel file
    df = pd.DataFrame(data=result)
    df = df.T
    df.to_excel("requests.xlsx")


main()
