### 껐다켰다 연습

from selenium import webdriver
from selenium.webdriver.common.by import By
import mysql.connector
import time
url ='http://testbot.ddns.net:5235/donga/dangbun/naver/dan'
options = webdriver.ChromeOptions()
driver = webdriver.Chrome('C:/stamp/chromedriver', options=options)
# driver.get(url)
open0 = False

while True:
    config = {
        'user': 'root',
        'password': 'Seoseoseo7!',
        'host': 'localhost',
        'port': '3306'
    }
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    cursor.execute(
        """
        select state from gookhwe_stuffs.test where id='1'
        """
    )
    state0 = int(cursor.fetchall()[0][0])
    print(f"{state0}  {open0}")

    if state0 == 0:
        if open0 == True:
            pass
        elif open0 == False:
            open0 = True

            success0= False
            while success0 == False:
                try:
                    url = 'http://testbot.ddns.net:5235/donga/dangbun/naver/dan'
                    options = webdriver.ChromeOptions()
                    driver = webdriver.Chrome('C:/stamp/chromedriver', options=options)
                    driver.get(url)
                    success0 = True
                except:
                    print('안열림')
                    time.sleep(0.5)

    if state0 == 1:
        if open0 == True:
            open0 = False
            driver.quit()
        if open0 == False:
            pass

    time.sleep(2)