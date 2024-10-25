from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import binascii, codecs
import mysql.connector
from datetime import date
from ToolBox import still_10
from database import cursor, db
blob_scrol = codecs.decode(b'', 'utf-8')
text_list = blob_scrol.strip().split('\n')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome('C:/stamp/chromedriver', options=options)

url = f'https://assembly.webcast.go.kr/main/player.asp?xcode=33&xcgcd=DCM00003321400A401&'
options = webdriver.ChromeOptions()
driver = webdriver.Chrome('C:/stamp/chromedriver', options=options)
driver.get(url)
time.sleep(5)
player_wrap = driver.find_element(By.CLASS_NAME, 'player_wrap')
player_box = player_wrap.find_element(By.CLASS_NAME, 'player_box ')
video_01 = player_box.find_element(By.ID, 'video_01')
player_view = video_01.find_element(By.CLASS_NAME, 'player_view ')
mediaBox_01 = player_view.find_element(By.ID, 'mediaBox_01')
YoonVideo_01 = mediaBox_01.find_element(By.ID, 'YoonVideo_01')
# button=YoonVideo_01.find_element(By.TAG_NAME,'button').click()
player_ctrl = video_01.find_element(By.CLASS_NAME, 'player_ctrl')
button_list = player_ctrl.find_element(By.TAG_NAME, 'ul')
smi_btn = button_list.find_element(By.ID, 'smi_btn')
# button = smi_btn.find_element(By.TAG_NAME, 'a').click()

go = False
while go == False:
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'smi_word')))

        go = True
        print('here')
    except:
        button = smi_btn.find_element(By.TAG_NAME, 'a').click()
        pass
viewSubtit = smi_btn.find_element(By.ID, 'viewSubtit')
time.sleep(3)
while True:
    text_list_10 = text_list[-10:]
    try:
        incont = viewSubtit.find_element(By.CLASS_NAME, 'incont')
        temp = incont.find_elements(By.TAG_NAME, 'p')
        temp_list = []
        for i in temp:
            temp_text = i.text.strip()
            if temp_text not in text_list_10:
                text0 = i.text.strip()
                temp_list.append(text0)
                blob_scrol += text0 + '\n'
        text_list = text_list + temp_list
        print(text_list)
        time.sleep(4)
    except Exception as e:
        print(e)
