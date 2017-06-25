import os
import time

from pip._vendor import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

def download_file(filename,URL,saveDir):
    print ("["+filename+"] started downloading.")
    startTime = time.time()
    reply = requests.get(URL,stream=True)
    with open(saveDir+filename,'wb') as file:
        for chunk in reply.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
    totalTime = (time.time())-startTime
    print ("["+filename+"] finished in ["+str(totalTime)+"]")
    
def file_exist(filename,saveDir):
    return os.path.isfile(saveDir+filename)
    
URLS = []
saveDir = "F:\\VulnHub VM's\\"
chromeOptions = webdriver.ChromeOptions()
# chromeOptions.a
prefs = {"download.default_directory" : saveDir}
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chrome_options=chromeOptions)
driver.get("https://www.vulnhub.com/")

WebDriverWait(driver,10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,".cookieWarningBox")))
driver.find_element_by_css_selector(".cookieWarningBox").find_element_by_css_selector(".pull-right").click()
while True:
    localHrefs = []
    downloads = driver.find_element_by_css_selector(".container").find_elements_by_css_selector(".download")
    for download in downloads:
        try:
            localHrefs.append(download.find_element_by_tag_name('a').get_attribute('href').split("#")[1])
        except:
            pass
    for localHref in localHrefs:
        lis = driver.find_element_by_id(localHref).find_element_by_css_selector(".modal-body").find_elements_by_tag_name('li')
        for li in lis:
            if "Download (Mirror)" in str(li.get_attribute("innerHTML")):
                URLS.append(li.find_element_by_tag_name('a').get_attribute('href'))
    driver.find_element_by_css_selector(".text-center.pagination").find_element_by_link_text("Next").click()
    driver.get(driver.current_url)
    if "#" in driver.current_url:
        print ("Starting Downloads.")
        driver.close()
        break

for URL in URLS:
    filename = URL.split("/")[len(URL.split("/"))-1]
    Head = requests.head(URL)
    if file_exist(filename,saveDir):
        try:
            print ("DISK=["+str(os.path.getsize(saveDir+filename))+"]          ONLINE=["+str(Head.headers['Content-Length'])+"]")
            if int(Head.headers['Content-Length']) == int(os.path.getsize(saveDir+filename)):
                print("Skipping ["+filename+"].")
                continue
            else:
                download_file(filename,URL,saveDir)
        except Exception as e:
            print (e)
    else:
        try:
            download_file(filename, URL, saveDir)
        except Exception as e:
            print (e)
print ("Completed!")        
