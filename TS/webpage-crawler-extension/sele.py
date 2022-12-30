from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import time

# from pyvirtualdisplay import Display
import pandas as pd
import requests
import os
import sys


# virtual display
# display = Display(visible=0, size=(800, 600))
# display.start()

def extractDigits(lst):
    return list(map(lambda el: [el], lst))


df = pd.DataFrame(extractDigits(os.listdir('C:/Users/Hadiy/OneDrive/Desktop/ASE-22/Control/webpage-crawler-extension/server/output')), columns=['website'])
#df = pd.read_csv(r"C:/Users/Hadiy/OneDrive/Desktop/ASE-22/csv/test.csv")
# extractDigits(os.listdir('/home/student/TrackerSift/UserStudy/output'))
#df = pd.DataFrame([[sys.argv[1]]], columns=["website"])


count = 0

for i in df.index:
    # try:
        if i < 0:
            pass
        else:
            dic = {}
            # extension filepath
            ext_file = "C:/Users/Hadiy/OneDrive/Desktop/ASE-22/TS/webpage-crawler-extension/extension"

            opt = webdriver.ChromeOptions()
            # devtools necessary for complete network stack capture
            opt.add_argument("--auto-open-devtools-for-tabs")
            # loads extension
            opt.add_argument("load-extension=" + ext_file)
            # important for linux
            opt.add_argument("--no-sandbox")

            dc = DesiredCapabilities.CHROME
            dc["goog:loggingPrefs"] = {"browser": "ALL"}

            os.mkdir("server/output/" + df["website"][i])
            driver = webdriver.Chrome(
                ChromeDriverManager().install(), options=opt, desired_capabilities=dc
            )
            requests.post(
                url="http://localhost:3003/complete", data={"website": df["website"][i]}
            )
            driver.get(r"https://www." + df["website"][i])

            time.sleep(15)

            # Collecting Metrics
            # 1: page HTML
            f= open("server/output/" + df["website"][i] + "/pageHTML.txt","w+")
            f.write(driver.page_source)
            f.close()
            # 2: page Errors
            f= open("server/output/" + df["website"][i] + "/pageErrors.txt","w+")
            f.write(driver.get_log("browser"))
            f.close()

            # driver.quit
            driver.quit()

            count += 1
            with open("logs.txt", "w") as log:
                log.write(str(count))
                log.close()
            print(r"Completed: " + str(i) + " website: " + df["website"][i])
    # except:
    #     try:
    #         driver.quit()
    #     except:
    #         pass
    #     print(r"Crashed: " + str(i) + " website: " + df["website"][i])
