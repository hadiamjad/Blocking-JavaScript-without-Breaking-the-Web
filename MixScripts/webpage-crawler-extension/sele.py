from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import time

from pyvirtualdisplay import Display
import pandas as pd
import requests
import os


# virtual display
display = Display(visible=0, size=(800, 600))
display.start()

df = pd.read_csv(r"02.csv")
# extractDigits(os.listdir('/home/student/TrackerSift/UserStudy/output'))
# df = pd.DataFrame([["washingtonpost.com/"]], columns=["website"])


count = 0

for i in df.index:
    try:
        if i < 0:
            pass
        else:
            dic = {}
            # extension filepath
            ext_file = "extension"

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
                url="http://localhost:3000/complete", data={"website": df["website"][i]}
            )
            driver.get(r"https://www." + df["website"][i])

            # sleep
            time.sleep(15)

            # dictionary collecting logs
            # 1: Logs 2: PageSource
            dic[df["website"][i]] = []
            # saving logs in dictionary
            dic[df["website"][i]].append(driver.get_log("browser"))
            dic[df["website"][i]].append(driver.page_source)
            # saving it in csv
            pd.DataFrame(dic).to_csv("server/output/" + df["website"][i] + "/logs.csv")
            # driver.quit
            driver.quit()

            count += 1
            with open("logs.txt", "w") as log:
                log.write(str(count))
                log.close()
            print(r"Completed: " + str(i) + " website: " + df["website"][i])
    except:
        try:
            driver.quit()
        except:
            pass
        print(r"Crashed: " + str(i) + " website: " + df["website"][i])
