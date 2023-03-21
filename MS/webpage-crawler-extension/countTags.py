from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os

def getMissingURLS(control_path, blocking_path):

    # Load the control setting HTML file
    with open(control_path, "r", encoding="utf-8") as f:
        control_html = f.read()

    # Load the blocking setting HTML file
    with open(blocking_path, "r", encoding="utf-8") as f:
        blocking_html = f.read()

    # Parse the HTML files with BeautifulSoup
    control_soup = BeautifulSoup(control_html, "html.parser")
    blocking_soup = BeautifulSoup(blocking_html, "html.parser")

    # Find all <img>, <video>, <iframe>, <script>, and <source> tags in the control setting HTML
    control_images = control_soup.find_all("img")
    control_videos = control_soup.find_all("video")
    control_iframes = control_soup.find_all("iframe")
    control_scripts = control_soup.find_all("script")
    control_sources = control_soup.find_all("source")

    # Find all <img>, <video>, <iframe>, <script>, and <source> tags in the blocking setting HTML
    blocking_images = blocking_soup.find_all("img")
    blocking_videos = blocking_soup.find_all("video")
    blocking_iframes = blocking_soup.find_all("iframe")
    blocking_scripts = blocking_soup.find_all("script")
    blocking_sources = blocking_soup.find_all("source")

    # Extract the URLs from the <img>, <video>, <iframe>, <script>, and <source> tags in the control setting HTML
    control_urls = {
        "img": [img.get("src", "") for img in control_images],
        "video": [vid.get("src", "") for vid in control_videos],
        "iframe": [iframe.get("src", "") for iframe in control_iframes],
        "script": [script.get("src", "") for script in control_scripts],
        "source": [source.get("src", "") for source in control_sources],
    }

    # Extract the URLs from the <img>, <video>, <iframe>, <script>, and <source> tags in the blocking setting HTML
    blocking_urls = {
        "img": [img.get("src", "") for img in blocking_images],
        "video": [vid.get("src", "") for vid in blocking_videos],
        "iframe": [iframe.get("src", "") for iframe in blocking_iframes],
        "script": [script.get("src", "") for script in blocking_scripts],
        "source": [source.get("src", "") for source in blocking_sources],
    }

    # Find the missing URLs
    missing_urls = {
        "img": list(set(control_urls["img"]) - set(blocking_urls["img"])),
        "video": list(set(control_urls["video"]) - set(blocking_urls["video"])),
        "iframe": list(set(control_urls["iframe"]) - set(blocking_urls["iframe"])),
        "script": list(set(control_urls["script"]) - set(blocking_urls["script"])),
        "source": list(set(control_urls["source"]) - set(blocking_urls["source"])),
    }

    return missing_urls

def extractDigits(lst):
    return list(map(lambda el: [el], lst))

def getURLLabel(url, control):
    for i in control.index:
        if url == control["http_req"][i]:
            if (control["easylistflag"][i] == 1 or control["easyprivacylistflag"][i] == 1 or control["ancestorflag"][i] == 1):
                return 1
            else:
                return 0
    return 0

def functionalMissingURLS(dic, missingfunctional_urls, control):
    for itm in dic:
        for url in dic[itm]:
            missingfunctional_urls[itm] += getURLLabel(url, control)
            

def main():
    df = pd.DataFrame(extractDigits(os.listdir('../../Control/webpage-crawler-extension/server/output')), columns=['website'])
    missingfunctional_urls = {
        "img": 0,
        "video": 0,
        "iframe": 0,
        "script": 0,
        "source": 0,
    }
    for j in df.index:
        try:
            control = '../../Control/webpage-crawler-extension/server/output/' + df["website"][j] + '/pageHTML.txt'
            blocking = 'server/output/' + df["website"][j] + '/pageHTML.txt'
            # Get the missing URLs
            missing_urls = getMissingURLS(control, blocking)
            # read netwrok json files
            control_req = pd.read_json('../../Control/webpage-crawler-extension/server/output/' + df["website"][j] + '/label_request.json')
            functionalMissingURLS(missing_urls, missingfunctional_urls, control_req)
        except:
            pass
    print(missingfunctional_urls)


main()