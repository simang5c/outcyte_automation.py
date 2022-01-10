#importing necessary packages
# in this case selenium python package

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import glob
import re
from json import dumps
from bs4 import BeautifulSoup
import pandas as pd

#providing the link
new_url0="http://www.outcyte.com"

#insert the supporting web browser driver *mozilla/chrome driver". In this case I use chromedriver
chromedriver = "/home/labor2/Desktop/chromedriver_linux64_1/chromedriver"
driver=webdriver.Chrome(chromedriver)
driver.implicitly_wait(100) #waiting to open the browser and go to the link
driver.get(new_url0)
fastas=glob.glob("*.fasta")
data_list = []

for fasta in fastas:
    with open(fasta, 'r') as myfile:
        data = myfile.read()
        print(data)
        search = driver.find_element_by_name('seq')
        search.clear()
        driver.execute_script(f"arguments[0].value={dumps(data)};",search)
        #search.send_keys(data)
        driver.find_element_by_xpath("//input[@type='submit']").click()
        html_s=driver.page_source
        soup=BeautifulSoup(html_s)
        table = soup.find_all('table')[0]
        df = pd.read_html(str(table),header=0)
        data_list.append(df[0])
        driver.execute_script("window.history.go(-1)") 

driver.quit()
#preparing the output files and writing to a file name ups_predicted_file.csv
result = pd.concat([pd.DataFrame(data_list[i]) for i in range(len(data_list))],ignore_index=True)
result.to_csv('ups_predicted_file.csv', sep='\t', index=False)
