from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import os
import requests
import cv2


MAX_RANGES_SCREEN = 500

keyword = "BNK48"
googleSearch = "https://www.google.co.in/search?q="+keyword+"&source=lnms&tbm=isch"
options = Options()
options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
#browser = webdriver.Chrome('chromedriver.exe')
browser = webdriver.Chrome('chromedriver.exe', chrome_options = options)
browser.get(googleSearch)
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

succounter = 0

# Start search
print("[INFO] searching images '{}' from Google with Chrome.. ".format(keyword))
print("[INFO] Check folder [{}] ...".format(keyword))
directory = os.path.join(os.getcwd(),keyword)

if not os.path.exists(directory):
    print("[INFO] Check folder [{}] there is not exists. ...".format(keyword))
    os.mkdir(directory)
    print("[INFO] Create folder [{}] successful. ...".format(keyword))

for _ in range(MAX_RANGES_SCREEN):
    browser.execute_script("window.scrollBy(0,10000)")

count = 0
for x in browser.find_elements_by_xpath('//div[contains(@class,"rg_meta")]'):
    print("[INFO] start saving image No. {}...".format(count))

    try:
        url = json.loads(x.get_attribute('innerHTML'))["ou"]
        print("[INFO] fetching: {}".format(url))
        requestFile = requests.get(url, timeout=30)
        fileName = keyword + '_' + str(count).zfill(6) + url[url.rfind("."):]
        saveDirectory = os.path.join(directory, fileName)
        f = open(saveDirectory, "wb")
        f.write(requestFile.content)
        f.close()
        image = cv2.imread(saveDirectory)

        if image is None:
            print("[INFO] deleting: {}...".format(fileName))
            os.remove(saveDirectory)
            continue
    except Exception as e:
        print("[ERR] Skipping >> URL {} doesn't load...".format(url))
        print("[ERR] {}... ".format(e))
        continue
    count += 1
